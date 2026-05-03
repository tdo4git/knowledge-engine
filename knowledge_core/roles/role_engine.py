from dataclasses import dataclass
from knowledge_core.intent.intent_engine import IntentResult


@dataclass
class Role:
    """
    Represents the advisory role used when generating an answer.
    """
    name: str
    description: str


ROLE_MAP = {
    "explain": Role(
        name="trusted_advisor",
        description="Explain regulatory or technical topics clearly and objectively."
    ),

    "compare": Role(
        name="analyst",
        description="Compare options or approaches objectively and highlight differences."
    ),

    "assess": Role(
        name="regulatory_advisor",
        description="Assess risks, compliance aspects, and regulatory implications."
    ),

    "recommend": Role(
        name="strategy_advisor",
        description="Provide strategic recommendations based on available knowledge."
    ),

    "summarize": Role(
        name="knowledge_summarizer",
        description="Summarize knowledge sources clearly and concisely."
    ),
}


class RoleEngine:
    """
    Role Engine maps Intent → Role.
    """

    def detect_role(self, intent: IntentResult) -> Role:
        if intent.interaction_intent in ROLE_MAP:
            return ROLE_MAP[intent.interaction_intent]

        return ROLE_MAP["explain"]