from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

def get_openai_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY missing")
    return key


CLASSIFIER_TEMPERATURE = 0.0
CLASSIFIER_MAX_TOKENS = 400

GOVERNANCE_REVIEW_MAX_TOKENS = 600