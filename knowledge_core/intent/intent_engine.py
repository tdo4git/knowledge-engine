from dataclasses import dataclass
from typing import Optional


@dataclass
class IntentResult:
    """
    Result object returned by the Intent Engine.
    """
    interaction_intent: str
    content_intent: str
    override: bool = False


# -----------------------------
# Interaction Intent Detection
# -----------------------------

def detect_interaction_intent(query: str) -> str:
    q = query.lower()

    if "compare" in q or "vergleich" in q:
        return "compare"

    if "recommend" in q or "empfehlen" in q:
        return "recommend"

    if "assess" in q or "bewerten" in q or "risiko" in q:
        return "assess"

    if "summarize" in q or "zusammenfassen" in q:
        return "summarize"

    return "explain"


# -----------------------------
# Content Intent Detection
# -----------------------------

def detect_content_intent(query: str) -> str:
    q = query.lower()

    if "anbieter" in q or "vendor" in q or "market" in q:
        return "market"

    if "vergleich" in q or "compare" in q:
        return "competitive"

    if "strategie" in q or "strategy" in q:
        return "strategy"

    if "portfolio" in q:
        return "portfolio"

    if "beratung" in q or "advisor" in q:
        return "advisory"

    return "normative"


# -----------------------------
# Public API
# -----------------------------

def detect_intent(query: str, content_override: Optional[str] = None) -> IntentResult:

    interaction = detect_interaction_intent(query)

    if content_override:
        return IntentResult(
            interaction_intent=interaction,
            content_intent=content_override,
            override=True
        )

    content = detect_content_intent(query)

    return IntentResult(
        interaction_intent=interaction,
        content_intent=content,
        override=False
    )