import re
from typing import Optional


# =========================================================
# DOC ID GENERATOR — TD-002
#
# Schema: doc_{origin_short}_{topic}_{year?}_{hash6}
#
# Garantien:
# - deterministisch (gleicher Input → gleicher Output)
# - eindeutig durch Hash-Suffix
# - lesbar durch Origin + Topic + Jahr
# =========================================================

def generate_doc_id(
    title: str,
    document_type: str,
    doc_hash: Optional[str] = None,
    origin: Optional[str] = None
) -> str:

    if not title:
        raise ValueError("Title must not be empty")

    if not document_type:
        raise ValueError("document_type must not be empty")

    title_clean = _normalize_text(title)

    origin_short = _normalize_origin(origin)
    topic = _extract_topic(title_clean)
    year = _extract_year(title_clean)
    hash_suffix = _extract_hash_suffix(doc_hash)

    parts = ["doc", origin_short, topic]

    if year:
        parts.append(year)

    parts.append(hash_suffix)

    return "_".join(parts)


# =========================================================
# HELPERS
# =========================================================

def _normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text.strip()


def _normalize_origin(origin: Optional[str]) -> str:
    """
    Kürzt Origin auf kompaktes Präfix.
    """
    mapping = {
        "legislator":           "eu",
        "supervisory_authority": "bafin",
        "consulting_firm":      "consulting",
        "cloud_vendor":         "aws",
        "software_vendor":      "vendor",
        "industry_association": "industry",
        "research_institution": "research",
        "internal":             "internal",
        "unknown":              "unknown",
    }
    return mapping.get(origin, "unknown") if origin else "unknown"


def _extract_topic(title: str) -> str:
    """
    Extracts a stable topic token from title.

    Strategy:
    1. Prefer known domain keywords (priority order)
    2. Fallback: first meaningful word
    """

    KEYWORDS = [
        "dora",
        "vait",
        "bait",
        "solvency",
        "cloud",
        "sovereignty",
        "insurance",
        "regulation",
        "outsourcing",
        "ai",
        "llm",
    ]

    for keyword in KEYWORDS:
        if keyword in title:
            return keyword

    words = re.findall(r"[a-z0-9]+", title)

    for word in words:
        if len(word) > 3:
            return word

    return "unknown"


def _extract_year(title: str) -> Optional[str]:
    match = re.search(r"(20\d{2})", title)
    return match.group(1) if match else None


def _extract_hash_suffix(doc_hash: Optional[str]) -> str:
    """
    Nimmt die ersten 6 Zeichen des doc_hash.
    Fallback: 'nohash' wenn kein Hash vorhanden.
    """
    if not doc_hash:
        return "nohash"
    return doc_hash[:6]