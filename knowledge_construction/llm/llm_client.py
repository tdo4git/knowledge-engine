import os
import json
import re
from typing import Any, Dict, Optional

import anthropic

from config.construction_config import (
    LLM_MODEL,
    LLM_TEMPERATURE
)
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")


class LLMClient:
    """
    Pure execution client — Anthropic Claude.
    - No prompt logic
    - Contract-driven usage
    - Robust JSON handling
    """

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = LLM_MODEL
        self.temperature = LLM_TEMPERATURE

    # -------------------------------------------------

    def run(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:

        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens or 1024

        # Anthropic API: system is a top-level param, not a message
        kwargs_call = dict(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )

        if system_prompt:
            kwargs_call["system"] = system_prompt

        response = self.client.messages.create(**kwargs_call)

        content = response.content[0].text.strip()

        cleaned = self._clean_json(content)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            raise ValueError(f"LLM returned invalid JSON:\n{content}")

    # -------------------------------------------------

    def _clean_json(self, content: str) -> str:
        cleaned = content.strip()
        cleaned = re.sub(r"```json\s*", "", cleaned)
        cleaned = re.sub(r"```", "", cleaned)
        return cleaned.strip()