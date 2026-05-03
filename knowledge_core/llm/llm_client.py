import os
from typing import Optional

import anthropic

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

# Model constant — single source of truth for query pipeline
ENGINE_LLM_MODEL = "claude-sonnet-4-6"
ENGINE_LLM_MAX_TOKENS = 2048
ENGINE_LLM_TEMPERATURE = 0.3


class LLMClient:
    """
    Query Pipeline LLM client — Anthropic Claude.

    Unterschied zu knowledge_construction/llm/llm_client.py:
    - gibt Text zurück (kein JSON)
    - höhere max_tokens für Antwortgenerierung
    - leicht erhöhte Temperatur für natürlichere Antworten
    """

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = ENGINE_LLM_MODEL

    # -------------------------------------------------

    def generate(self, prompt: str) -> str:
        """
        Wird von QueryPipeline.run() aufgerufen.
        Prompt enthält SYSTEM ROLE + CONTEXT + INSTRUCTIONS + QUESTION.
        """

        response = self.client.messages.create(
            model=self.model,
            max_tokens=ENGINE_LLM_MAX_TOKENS,
            temperature=ENGINE_LLM_TEMPERATURE,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip()