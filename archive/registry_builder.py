import json
from pathlib import Path


class RegistryBuilder:

    def __init__(self, registry_path):

        self.registry_path = Path(registry_path)

        if self.registry_path.exists():
            with open(self.registry_path, "r", encoding="utf-8") as f:
                self.registry = json.load(f)
        else:
            self.registry = []

    # ----------------------------------------

    def add_document(self, metadata, classification):
        """
        metadata:
            - doc_id (REQUIRED, generated in pipeline)
            - title
            - source_file
            - optional: year, doc_hash

        classification:
            - result of classification + governance + enrichment
        """

        # 🔥 Single Source of Truth: doc_id comes from pipeline
        doc_id = metadata.get("doc_id")

        if not doc_id:
            raise ValueError("doc_id must be provided in metadata")

        entry = {

            "doc_id": doc_id,

            "title": metadata.get("title"),
            "source_file": metadata.get("source_file"),
            "year": metadata.get("year"),

            "origin": classification.get("origin"),
            "document_type": classification.get("document_type"),

            "knowledge_domain": classification.get("knowledge_domain"),
            "content_domain": classification.get("content_domain"),

            "vendor": classification.get("vendor"),

            "confidence_level": classification.get("confidence_level"),
            "confidentiality": classification.get("confidentiality"),

            "doc_hash": metadata.get("doc_hash")
        }

        self._check_duplicate(entry)

        self.registry.append(entry)

        return entry

    # ----------------------------------------

    def save(self):

        self.registry_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, indent=2)

    # ----------------------------------------

    def _check_duplicate(self, entry):

        for doc in self.registry:

            if doc.get("doc_hash") and doc["doc_hash"] == entry.get("doc_hash"):
                raise ValueError(
                    f"Document already exists in registry: {entry.get('source_file')}"
                )