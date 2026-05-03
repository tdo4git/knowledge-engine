from typing import Dict, List

from config.construction_config import REVIEW_LOW_CONFIDENCE_THRESHOLD


# ------------------------------------------------
# REVIEW DECISION ENGINE
# ------------------------------------------------
def review_decision(classification: Dict) -> Dict:
    """
    Determines whether a document requires manual review.

    Rules:
    - Low confidence → review
    - Unknown document type → review
    - Unknown origin → review

    Threshold is configured in config/construction_config.py:
    REVIEW_LOW_CONFIDENCE_THRESHOLD
    """

    reasons: List[str] = []

    confidence = classification.get("confidence")
    document_type = classification.get("document_type")
    origin = classification.get("origin")

    # ----------------------------------
    # 1. Low confidence
    # ----------------------------------

    if confidence is not None:
        try:
            if float(confidence) < REVIEW_LOW_CONFIDENCE_THRESHOLD:
                reasons.append("low_confidence")
        except (TypeError, ValueError):
            reasons.append("invalid_confidence")

    # ----------------------------------
    # 2. Unknown classification
    # ----------------------------------

    if document_type == "unknown":
        reasons.append("unknown_document_type")

    # ----------------------------------
    # 3. Missing or unknown origin
    # ----------------------------------

    if not origin or origin == "unknown":
        reasons.append("unknown_origin")

    # ----------------------------------
    # FINAL DECISION
    # ----------------------------------

    review_required = len(reasons) > 0

    return {
        "review_required": review_required,
        "review_reasons": reasons
    }