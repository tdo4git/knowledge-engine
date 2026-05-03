import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_PATH = Path(__file__).resolve().parent.parent
AI_SUGGESTION_PATH = BASE_PATH / "tests/onboarding_ai_suggestions"
INTAKE_PATH = BASE_PATH / "knowledge_sources/intake"


def sanitize_filename(name):
    name = name.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"\s+", "_", name)
    return name


TAXONOMY = {
    "document_type": ["regulatory_text", "consulting_framework"],
    "origin": ["legislator", "consulting_firm"],
    "knowledge_domain": ["insurance_domain", "trusted_advisor"],
    "content_domain": ["risk_management", "compliance"]
}


def main():

    print("\n=== AI REGISTRY SUGGESTER ===\n")

    files = list(INTAKE_PATH.glob("*"))
    print(f"→ Found {len(files)} documents")

    AI_SUGGESTION_PATH.mkdir(parents=True, exist_ok=True)

    for file in files:

        prompt = f"""
Use ONLY values from this taxonomy:

{json.dumps(TAXONOMY, indent=2)}

Return STRICT JSON with:
document_type, origin, knowledge_domain, content_domain

Document:
{file.name}
"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        filename = sanitize_filename(file.name)
        path = AI_SUGGESTION_PATH / f"{filename}.json"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        print(f"✔ AI suggestion created: {file.name}")


if __name__ == "__main__":
    main()