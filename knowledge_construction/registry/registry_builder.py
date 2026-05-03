import json
from pathlib import Path
from typing import Dict, List


KEEP_FIELDS: List[str] = [
    "document_type",
    "knowledge_domain",
    "origin",
    "jurisdiction",
    "confidence",
    "bias",
    "domain_layer"
]


class RegistryBuilder:

    def __init__(self, registry_path: str):
        self.registry_path = Path(registry_path)

        if self.registry_path.exists():
            with open(self.registry_path, "r", encoding="utf-8") as f:
                self.registry = json.load(f)
        else:
            self.registry = []

    # ------------------------------------------------

    def add_document(self, metadata: Dict, classification: Dict) -> Dict:

        doc_id = metadata.get("doc_id")
        title = metadata.get("title")
        source_file = metadata.get("source_file")
        doc_hash = metadata.get("doc_hash")

        if not doc_id:
            raise ValueError("doc_id must be provided in metadata")

        if not source_file:
            raise ValueError(f"source_file missing for doc_id={doc_id}")

        filtered_classification = {
            key: classification.get(key)
            for key in KEEP_FIELDS
        }

        entry = {
            "doc_id": doc_id,
            "title": title,
            "source_file": source_file,
            "doc_hash": doc_hash,
            **filtered_classification
        }

        self._check_duplicate(entry)

        self.registry.append(entry)

        return entry

    # ------------------------------------------------

    def get_by_source_file(self, source_file: str):

        for doc in self.registry:
            if doc.get("source_file") == source_file:
                return doc

        return None

    # ------------------------------------------------

    def save(self):

        self.registry_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, indent=2)

    # ------------------------------------------------

    def _check_duplicate(self, entry: Dict):
        """
        Duplikat-Prüfung in zwei Stufen:
        1. doc_hash — erkennt umbenannte Dateien
        2. source_file — Fallback wenn kein Hash vorhanden
        """

        for doc in self.registry:

            # Hash-basierte Prüfung (primär)
            if entry.get("doc_hash") and doc.get("doc_hash"):
                if doc["doc_hash"] == entry["doc_hash"]:
                    raise ValueError(
                        f"Duplicate document detected (hash match): "
                        f"existing='{doc.get('source_file')}' "
                        f"new='{entry.get('source_file')}'"
                    )

            # Dateiname-Fallback
            if doc.get("source_file") == entry.get("source_file"):
                raise ValueError(
                    f"Document already exists in registry: {entry.get('source_file')}"
                )