from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class QueryContext:
    """
    Central state object for a single query execution.

    The QueryContext collects all intermediate results produced by the
    QueryPipeline so that the full reasoning path of a query remains
    traceable and debuggable.

    This structure also enables future features such as:
    - explainability reports
    - audit logging
    - monitoring
    - evaluation pipelines
    """

    # --------------------------------------------------
    # Input
    # --------------------------------------------------

    query: str

    # --------------------------------------------------
    # Intent & Role
    # --------------------------------------------------

    intent: Optional[str] = None
    role: Optional[str] = None

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------

    retrieval_result: Optional[Any] = None
    ranked_documents: Optional[List[Any]] = None

    # --------------------------------------------------
    # Perspective
    # --------------------------------------------------

    perspective: Optional[str] = None

    # --------------------------------------------------
    # Context Construction
    # --------------------------------------------------

    context_package: Optional[Any] = None

    # --------------------------------------------------
    # Prompt & LLM
    # --------------------------------------------------

    prompt: Optional[str] = None
    response: Optional[str] = None
