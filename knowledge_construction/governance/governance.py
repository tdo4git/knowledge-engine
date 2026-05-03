from pathlib import Path


def enforce_internal_origin(title: str, preview_text: str, result: dict) -> dict:
    """
    Deterministic override rules for origin detection.
    Prevents LLM misclassification.
    """

    text = f"{title} {preview_text}".lower()

    # simple internal detection
    if "internal strategy" in text or "internal document" in text:
        result["origin"] = "internal"

    return result