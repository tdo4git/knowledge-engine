import json
from pathlib import Path
from datetime import datetime
from typing import Dict


class ReviewLogger:
    """
    Logs review decisions into audit log.

    Purpose:
    - Persist review_required + reasons
    - Keep registry clean
    - Enable traceability
    """

    def __init__(self, audit_path: Path):
        self.audit_path = audit_path
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------

    def log_review(
        self,
        doc_id: str,
        review_info: Dict
    ):
        """
        Writes a single review decision entry.
        """

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "doc_id": doc_id,
            "review_required": review_info.get("review_required"),
            "review_reasons": review_info.get("review_reasons", [])
        }

        with open(self.audit_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")