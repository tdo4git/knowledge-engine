import json
import dataclasses
from datetime import datetime


def _serialize(obj):
    """
    JSON serializer for dataclasses and objects with __dict__.
    """
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return str(obj)


class RetrievalDecisionLogger:

    def __init__(self, log_path):
        self.log_path = log_path

    def log(self, query, intent, role, ranked_documents, context_package):

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "intent": _serialize(intent),
            "role": _serialize(role),
            "retrieved_documents": [
                {
                    "doc_id": doc.doc_id,
                    "semantic_score": doc.semantic_score,
                    "governance_score": doc.governance_score,
                    "final_score": doc.score
                }
                for doc in ranked_documents
            ],
            "context_chunks": [
                {
                    "doc_id": chunk.doc_id,
                    "chunk_id": chunk.chunk_id
                }
                for chunk in context_package.chunks
            ],
            "sources": context_package.sources
        }

        with open(self.log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")