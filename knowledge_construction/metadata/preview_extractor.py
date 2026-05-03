from pathlib import Path

from config.construction_config import PREVIEW_MAX_CHARS

from knowledge_construction.document_processing.document_text_extractor import (
    extract_document_text,
)


# ------------------------------------------------
# TEXT CLEANING (ALIGN WITH DOCUMENT EXTRACTOR)
# ------------------------------------------------
def _clean_text(text: str) -> str:
    """
    Lightweight normalization for preview usage.
    Keeps consistent with document_text_extractor.
    """

    return (
        text.replace("\n", " ")
        .replace("\r", " ")
        .strip()
    )


# ------------------------------------------------
# PUBLIC API
# ------------------------------------------------
def extract_preview(file_path: Path) -> str:
    """
    Extracts preview text based on full document text.

    Strategy:
    - use full text extraction (single source of truth)
    - clean text
    - truncate via config

    This avoids inconsistencies between preview and full-text processing.
    """

    file_path = Path(file_path)

    try:
        full_text = extract_document_text(file_path)

    except Exception:
        print(f"⚠ Failed to extract document text: {file_path.name}")
        return ""

    if not full_text:
        return ""

    cleaned = _clean_text(full_text)

    # config-driven truncation
    preview = cleaned[:PREVIEW_MAX_CHARS]

    return preview