from typing import Dict

from config.taxonomy import (
    KNOWLEDGE_DOMAINS,
    DOCUMENT_TYPES,
    DOMAIN_LAYERS,
    ORIGINS,
    JURISDICTIONS,
    BIAS_LEVELS
)


# =========================================================
# VALIDATION – ENUM & STRUCTURE
# =========================================================

REQUIRED_FIELDS = [
    "document_type",
    "domain_layer",
    "knowledge_domain",
    "origin",
    "jurisdiction",
    "confidence"
]


def validate_enums(result: Dict):
    """
    Validates classification output against taxonomy.

    Strict:
    - required fields must exist
    - values must match taxonomy
    - confidence must be numeric and within [0, 1]

    No mutation. Raises ValueError on failure.
    """

    # -------------------------------------------------
    # 1. Required fields
    # -------------------------------------------------

    for field in REQUIRED_FIELDS:
        if field not in result:
            raise ValueError(f"Missing required field: {field}")

    # -------------------------------------------------
    # 2. Enum validation
    # -------------------------------------------------

    _validate_enum(result, "document_type", DOCUMENT_TYPES)
    _validate_enum(result, "domain_layer", DOMAIN_LAYERS)
    _validate_enum(result, "knowledge_domain", KNOWLEDGE_DOMAINS)
    _validate_enum(result, "origin", ORIGINS)
    _validate_enum(result, "jurisdiction", JURISDICTIONS)

    # -------------------------------------------------
    # 3. Optional fields
    # -------------------------------------------------

    if "bias_level" in result and result["bias_level"] is not None:
        _validate_enum(result, "bias_level", BIAS_LEVELS)

    # -------------------------------------------------
    # 4. Confidence validation
    # -------------------------------------------------

    _validate_confidence(result.get("confidence"))


# =========================================================
# HELPERS
# =========================================================

def _validate_enum(result: Dict, field: str, allowed_values):
    value = result.get(field)

    if value is None:
        raise ValueError(f"{field} must not be None")

    if value not in allowed_values:
        raise ValueError(
            f"Invalid {field}: {value} | allowed: {allowed_values}"
        )


def _validate_confidence(value):
    if value is None:
        raise ValueError("confidence must not be None")

    if not isinstance(value, (int, float)):
        raise ValueError(f"confidence must be numeric, got: {type(value)}")

    if not (0.0 <= float(value) <= 1.0):
        raise ValueError(f"confidence out of range: {value}")