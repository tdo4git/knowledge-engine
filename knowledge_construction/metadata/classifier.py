import json
import re
from typing import Dict
from pathlib import Path

from knowledge_construction.validation.validation import validate_enums

from config.construction_config import (
    CLASSIFIER_TEMPERATURE,
    CLASSIFIER_MAX_TOKENS,
    PREVIEW_MAX_CHARS          # ← import erzwingt bewussten Umgang mit Preview-Größe
)
from config.governance_config import LLM_DOMAIN_NORMALIZATION

from knowledge_construction.llm.contract_loader import load_contract_by_task
from knowledge_construction.llm.prompt_builder import build_prompt


def classify_document(
    title: str,
    preview_text: str,
    llm_client,
    file_path: Path
) -> Dict:
    """
    FINAL PRODUCTION CLASSIFIER

    Responsibilities:
    - Build LLM prompt from contract
    - Execute classification
    - Normalize output
    - Ensure schema consistency

    IMPORTANT:
    - NO governance logic here
    - NO review logic here

    Preview-Truncation:
    - Die Größe des preview_text wird AUSSCHLIESSLICH durch
      PREVIEW_MAX_CHARS in construction_config.py gesteuert.
    - Kein hardcodiertes Truncation hier. Wer die Preview-Größe
      ändern will, ändert die Config — nicht den Classifier.
    """

    # -------------------------------------------------
    # Guard: preview_text darf nicht stiller truncated werden
    # -------------------------------------------------
    assert isinstance(preview_text, str), "preview_text must be a string"

    # -------------------------------------------------
    # 1. Load contract
    # -------------------------------------------------

    contract = load_contract_by_task("classification")

    # -------------------------------------------------
    # 2. Build context
    # Preview-Größe kommt aus PREVIEW_MAX_CHARS (via preview_extractor).
    # Kein [:N] hier — Single Source of Truth ist die Config.
    # -------------------------------------------------

    context = f"""
Title: {title}

Preview:
{preview_text}
""".strip()

    # -------------------------------------------------
    # 3. Build prompt
    # -------------------------------------------------

    prompt = build_prompt(
        query="",
        context=context,
        contract=contract
    )

    try:

        # -------------------------------------------------
        # 4. LLM Call (config-driven)
        # -------------------------------------------------

        response = llm_client.run(
            prompt=prompt["user"],
            system_prompt=prompt["system"],
            temperature=CLASSIFIER_TEMPERATURE,
            max_tokens=CLASSIFIER_MAX_TOKENS
        )

        if not response:
            raise ValueError("Empty LLM response")

        # -------------------------------------------------
        # 5. Normalize response
        # -------------------------------------------------

        result = _normalize_response(response)
        result = _normalize_confidence(result)
        result = _normalize_domain(result)      # TD: LLM domain normalization

        # -------------------------------------------------
        # 6. Final validation (LLM output only!)
        # -------------------------------------------------

        validate_enums(result)

        return result

    except Exception as e:

        print(f"\n❌ Classification failed: {e}")
        print("\nRaw LLM output:\n")
        print(response if "response" in locals() else "No response")

        raise


# ------------------------------------------------
# HELPERS
# ------------------------------------------------

def _normalize_domain(result: Dict) -> Dict:
    """
    Mappt ungültige LLM-Ausgaben auf gültige KNOWLEDGE_DOMAINS.
    Claude verwendet präzise Topic-Begriffe die nicht in der
    Taxonomie stehen — diese werden hier korrigiert.
    """
    current = result.get("knowledge_domain")

    if current and current in LLM_DOMAIN_NORMALIZATION:
        normalized = LLM_DOMAIN_NORMALIZATION[current]
        print(f"  ↳ Domain normalization: {current} → {normalized}")
        result["knowledge_domain"] = normalized

    return result


def _normalize_confidence(result: Dict) -> Dict:
    """
    Ensures confidence is always numeric (float)
    """

    value = result.get("confidence")

    if isinstance(value, (int, float)):
        return result

    if isinstance(value, str):

        mapping = {
            "high": 0.9,
            "medium": 0.6,
            "low": 0.3
        }

        result["confidence"] = mapping.get(value.lower(), 0.5)

    else:
        result["confidence"] = 0.5

    return result


def _normalize_response(response) -> Dict:
    """
    Ensures consistent dict output from LLM
    """

    if isinstance(response, dict):
        return response

    cleaned = _clean_json_response(response)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from LLM: {e}")


def _clean_json_response(response: str) -> str:
    """
    Removes markdown / formatting artifacts
    """

    cleaned = response.strip()

    cleaned = re.sub(r"^```json\s*", "", cleaned)
    cleaned = re.sub(r"^```", "", cleaned)
    cleaned = re.sub(r"```$", "", cleaned)

    return cleaned.strip()