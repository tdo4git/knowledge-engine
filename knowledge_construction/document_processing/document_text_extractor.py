from pathlib import Path
from typing import Optional

from pypdf import PdfReader
from docx import Document


# ------------------------------------------------
# Text Cleaning (NEU)
# ------------------------------------------------

def _clean_text(text: str) -> str:
    return (
        text
        .replace("\n", " ")
        .replace("\t", " ")
        .replace("[UNK]", "")
        .replace("  ", " ")
        .strip()
    )


# ------------------------------------------------
# Public API
# ------------------------------------------------

def extract_document_text(file_path: Path) -> str:
    """
    Extracts full text from supported document types.
    Applies basic cleaning before returning.
    """

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        text = _extract_pdf(file_path)
        return _clean_text(text)

    if suffix == ".docx":
        text = _extract_docx(file_path)
        return _clean_text(text)

    if suffix in [".txt", ".md"]:
        text = _extract_text(file_path)
        return _clean_text(text)

    raise ValueError(f"Unsupported file type: {suffix}")


# ------------------------------------------------
# PDF
# ------------------------------------------------

def _extract_pdf(file_path: Path) -> str:

    reader = PdfReader(file_path)

    text_parts = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text_parts.append(page_text)

    return "\n".join(text_parts)


# ------------------------------------------------
# DOCX
# ------------------------------------------------

def _extract_docx(file_path: Path) -> str:

    doc = Document(file_path)

    text_parts = []

    for p in doc.paragraphs:
        if p.text.strip():
            text_parts.append(p.text)

    return "\n".join(text_parts)


# ------------------------------------------------
# TXT / MD
# ------------------------------------------------

def _extract_text(file_path: Path) -> str:

    return file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )