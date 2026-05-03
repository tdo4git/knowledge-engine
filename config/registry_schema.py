# config/registry_schema.py

KEEP_FIELDS = [
    "doc_id",
    "title",
    "source_file",
    "document_type",
    "knowledge_domain",
    "origin",
    "jurisdiction",
    "confidence",
    "bias",
    "domain_layer",
]


def filter_registry_fields(metadata: dict) -> dict:
    """
    Enforces strict registry schema.
    Drops all non-allowed fields.
    """
    return {k: metadata[k] for k in KEEP_FIELDS if k in metadata}