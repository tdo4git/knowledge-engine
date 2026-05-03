def governance_review(document_metadata: dict, *args, **kwargs) -> dict:

    # Minimal MVP Governance Review

    result = {
        "approved": True,
        "issues": []
    }

    # Optional: Check for doc_id (aber nicht blockierend!)
    if "doc_id" not in document_metadata:
        result["issues"].append("Missing doc_id")

    return result