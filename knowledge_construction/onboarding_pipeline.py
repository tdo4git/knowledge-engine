from pathlib import Path
import json
import shutil
from datetime import datetime

from knowledge_construction.metadata.preview_extractor import extract_preview
from knowledge_construction.metadata.classifier import classify_document
from knowledge_construction.metadata.doc_id_generator import generate_doc_id
from knowledge_construction.metadata_extractor import MetadataExtractor

from knowledge_construction.governance.governance_pipeline import apply_governance_pipeline

from knowledge_construction.document_processing.document_text_extractor import extract_document_text

from knowledge_construction.validation.validation import validate_enums
from knowledge_construction.validation.cross_field_rules import validate_cross_field

from knowledge_construction.registry.registry_builder import RegistryBuilder
from knowledge_construction.audit.audit_logger import log_classification
from knowledge_construction.audit.review_logger import ReviewLogger
from knowledge_construction.review.review_decision import review_decision

from knowledge_construction.chunking.chunker import Chunker
from knowledge_construction.embedding.embedding_generator import EmbeddingGenerator
from knowledge_construction.embedding.index_consistency_check import IndexConsistencyCheck

from config.construction_config import CHUNKS_PATH

ARCHIVE_PATH = Path("knowledge_sources/archive")
REVIEW_REPORT_PATH = Path("knowledge_base/audit/review_report.txt")


class OnboardingPipeline:

    def __init__(self, registry_path: str, llm_client):

        self.registry_builder = RegistryBuilder(registry_path)
        self.llm_client = llm_client
        self.metadata_extractor = MetadataExtractor()

        self.chunker = Chunker()
        self.embedding_generator = EmbeddingGenerator()
        self.index_checker = IndexConsistencyCheck()

        self.review_logger = ReviewLogger(
            Path("knowledge_base/audit/onboarding_review.jsonl")
        )

        self.ai_suggestion_path = Path("tests/onboarding_ai_suggestions")
        self.ai_suggestion_path.mkdir(parents=True, exist_ok=True)

        # Sammelt Review-Punkte über alle Dokumente des Laufs
        self._review_items = []

    # -------------------------------------------------

    def process_document(self, file_path: str):

        file_path = Path(file_path)

        print(f"\nProcessing document: {file_path.name}")

        # -------------------------------------------------
        # 0. EXISTING CHECK (idempotent)
        # -------------------------------------------------

        existing = self.registry_builder.get_by_source_file(file_path.name)
        is_new_document = existing is None

        if existing:
            doc_id = existing["doc_id"]
            print(f"ℹ Existing document → reuse doc_id: {doc_id}")
        else:
            doc_id = None

        # -------------------------------------------------
        # 1. Preview
        # -------------------------------------------------

        preview_text = extract_preview(file_path)

        # -------------------------------------------------
        # 2. Classification (LLM)
        # -------------------------------------------------

        raw_classification = classify_document(
            title=file_path.stem,
            preview_text=preview_text,
            llm_client=self.llm_client,
            file_path=file_path
        )

        # -------------------------------------------------
        # 3. File Metadata (doc_hash)
        # -------------------------------------------------

        file_metadata = self.metadata_extractor.extract(file_path)
        doc_hash = file_metadata.get("doc_hash")

        # -------------------------------------------------
        # 4. Governance
        # -------------------------------------------------

        classification, review_info = apply_governance_pipeline(
            result=raw_classification,
            title=file_path.stem,
            preview_text=preview_text,
            file_path=file_path
        )

        # -------------------------------------------------
        # 5. doc_id (nur wenn neu)
        # -------------------------------------------------

        if is_new_document:
            doc_id = generate_doc_id(
                title=file_path.stem,
                document_type=classification["document_type"],
                doc_hash=doc_hash,
                origin=classification.get("origin")
            )

        # -------------------------------------------------
        # 6. AI Suggestion speichern
        # -------------------------------------------------

        self._save_ai_suggestion(doc_id, file_path, raw_classification)

        # -------------------------------------------------
        # 7. VALIDATION — blockiert bei Fehler (TD-003)
        # -------------------------------------------------

        validation_error = None

        try:
            validate_enums(classification)
            validate_cross_field(classification)
        except Exception as e:
            validation_error = str(e)
            print(f"⚠ Validation error: {validation_error}")

        if validation_error:
            # Dokument bleibt in intake — kein Registry-Eintrag, keine Archivierung
            self._review_items.append({
                "file": file_path.name,
                "doc_id": doc_id,
                "reason": "validation_error",
                "detail": validation_error
            })

            log_classification({
                "file": file_path.name,
                "doc_id": doc_id,
                "classification": classification,
                "review": {"review_required": True, "review_reasons": ["validation_error"]},
                "validation_error": validation_error,
                "is_new": is_new_document
            })

            raise ValueError(f"Validation failed: {validation_error}")

        # -------------------------------------------------
        # 8. Review Decision (Audit-Signal, kein harter Stop)
        # -------------------------------------------------

        review_decision_result = review_decision(classification)
        review_info.update(review_decision_result)

        self.review_logger.log_review(
            doc_id=doc_id,
            review_info=review_info
        )

        if review_info.get("review_required"):
            self._review_items.append({
                "file": file_path.name,
                "doc_id": doc_id,
                "reason": "review_required",
                "detail": review_info.get("review_reasons", [])
            })

        # -------------------------------------------------
        # 9. Registry (nur bei neu)
        # -------------------------------------------------

        if is_new_document:

            metadata = {
                "doc_id": doc_id,
                "title": file_path.stem,
                "source_file": file_path.name,
                "doc_hash": doc_hash
            }

            entry = self.registry_builder.add_document(
                metadata,
                classification
            )

            self.registry_builder.save()

            print(f"✔ New document added to registry: {doc_id}")

        else:
            entry = existing
            print(f"✔ Existing registry entry reused: {doc_id}")

        # -------------------------------------------------
        # 10. Chunking + Embedding (nur bei neu)
        # -------------------------------------------------

        if is_new_document:

            document_text = extract_document_text(file_path)

            chunks = self.chunker.chunk_document(
                document_text,
                doc_id
            )

            self.chunker.save_chunks(
                chunks,
                CHUNKS_PATH
            )

            self.embedding_generator.run()
            self.index_checker.run()

            print(f"✔ Chunks created: {len(chunks)}")

        else:
            print("ℹ Skipping chunking/embedding (already processed)")

        # -------------------------------------------------
        # 11. Archivierung — nur bei neuen, validen Dokumenten (TD-003)
        # -------------------------------------------------

        if is_new_document:
            self._archive_document(file_path)

        # -------------------------------------------------
        # 12. Audit Log
        # -------------------------------------------------

        log_classification({
            "file": file_path.name,
            "doc_id": doc_id,
            "classification": classification,
            "review": review_info,
            "validation_error": validation_error,
            "is_new": is_new_document
        })

        print(f"\n✔ Document processed: {doc_id}")

        return entry

    # -------------------------------------------------
    # ARCHIVIERUNG
    # -------------------------------------------------

    def _archive_document(self, file_path: Path):
        """
        Verschiebt ein erfolgreich verarbeitetes Dokument
        von intake/ nach archive/.
        """
        ARCHIVE_PATH.mkdir(parents=True, exist_ok=True)

        target = ARCHIVE_PATH / file_path.name

        if target.exists():
            print(f"ℹ Archive already contains: {file_path.name} — skipping move")
            return

        shutil.move(str(file_path), str(target))
        print(f"📦 Archived: {file_path.name}")

    # -------------------------------------------------
    # REVIEW REPORT
    # -------------------------------------------------

    def write_review_report(self):
        """
        Schreibt einen Review-Report nach jedem Onboarding-Lauf.
        Wird von run_onboarding.py aufgerufen.
        """

        REVIEW_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(REVIEW_REPORT_PATH, "w", encoding="utf-8") as f:

            f.write("ONBOARDING REVIEW REPORT\n")
            f.write(f"Generated: {datetime.utcnow().isoformat()}\n")
            f.write("=" * 50 + "\n\n")

            if not self._review_items:
                f.write("✔ Keine Review-Punkte — alle Dokumente sauber verarbeitet.\n")
                return

            f.write(f"{len(self._review_items)} Dokument(e) benoetigen Aufmerksamkeit:\n\n")

            for item in self._review_items:
                f.write(f"Datei:   {item['file']}\n")
                f.write(f"Doc-ID:  {item['doc_id']}\n")
                f.write(f"Grund:   {item['reason']}\n")
                f.write(f"Detail:  {item['detail']}\n")
                f.write("-" * 40 + "\n")

    # -------------------------------------------------

    def _save_ai_suggestion(self, doc_id, file_path, classification):

        file = self.ai_suggestion_path / f"{doc_id}.json"

        if file.exists():
            return

        data = {
            "doc_id": doc_id,
            "title": file_path.stem,
            "ai": classification
        }

        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)