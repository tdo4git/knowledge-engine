from pathlib import Path
from typing import Tuple, Dict

from knowledge_construction.governance.governance import enforce_internal_origin
from knowledge_construction.governance.governance_rules import apply_governance
from knowledge_construction.governance.bias import derive_bias


# ------------------------------------------------
# GOVERNANCE PIPELINE
# ------------------------------------------------
def apply_governance_pipeline(
    result: dict,
    title: str,
    preview_text: str,
    file_path: Path
) -> Tuple[Dict, Dict]:
    """
    FINAL governance pipeline (single entry point)

    Responsibilities:
    - enforce internal overrides
    - apply rule engine
    - derive secondary attributes
    - extract review signals (for audit layer)

    Returns:
    - cleaned_result (for registry)
    - review_info (for audit logging)
    """

    # ----------------------------------
    # 0. defaults (stability + SOURCE FIX)
    # ----------------------------------

    result.setdefault("origin", "unknown")

    # 🔥 CRITICAL FIX: ensure source tracking exists
    # Without this, priority logic does not work correctly
    for field in ["origin", "jurisdiction", "knowledge_domain"]:
        source_field = f"{field}_source"

        if field in result and source_field not in result:
            result[source_field] = "llm"

    # ----------------------------------
    # 1. deterministic overrides (pre-rules)
    # ----------------------------------

    result = enforce_internal_origin(
        title=title,
        preview_text=preview_text,
        result=result
    )

    # ----------------------------------
    # 2. central governance engine
    # ----------------------------------

    result = apply_governance(
        result=result,
        title=title,
        preview_text=preview_text,
        file_path=file_path
    )

    # ----------------------------------
    # 3. derived attributes
    # ----------------------------------

    result["bias"] = derive_bias(result.get("origin", "unknown"))

    # ----------------------------------
    # 4. extract review signals (strict separation)
    # ----------------------------------

    review_info = {
        "review_required": result.pop("review_required", False),
        "review_reasons": result.pop("review_reasons", [])
    }

    return result, review_info