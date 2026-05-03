import json
from pathlib import Path
from datetime import datetime


AUDIT_LOG_PATH = Path("knowledge_base/audit/onboarding_audit_log.jsonl")


def log_classification(event: dict):
    """
    Writes an onboarding event to the audit log.

    Uses JSONL format so entries can be appended efficiently.
    """

    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        **event
    }

    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record))
        f.write("\n")