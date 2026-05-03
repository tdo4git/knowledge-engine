from knowledge_core.intent.intent_engine import IntentEngine
from knowledge_core.roles.role_engine import RoleEngine
from knowledge_core.retrieval.retrieval_engine import RetrievalEngine
from knowledge_core.scoring.scoring_engine import ScoringEngine
from knowledge_core.perspective.perspective_orchestrator import PerspectiveOrchestrator
from knowledge_core.pipeline.context_builder import ContextBuilder
from knowledge_core.prompt.prompt_governance import PromptBuilder
from knowledge_core.pipeline.query_pipeline import QueryPipeline


class KnowledgeEngine:
    """
    Central entry point for the Strategic Knowledge Engine.

    This class wires together all engine components and exposes
    a simple interface:

        engine = KnowledgeEngine(...)
        ctx = engine.query("...")

    It encapsulates the full QueryPipeline.
    """

    def __init__(
        self,
        knowledge_base,
        embedding_model,
        llm_client,
        log_path="knowledge_base/audit/query_audit_log.jsonl"
    ):

        # --------------------------------------------------
        # Core Engines
        # --------------------------------------------------

        self.intent_engine = IntentEngine()
        self.role_engine = RoleEngine()

        self.retrieval_engine = RetrievalEngine(
            knowledge_base=knowledge_base,
            embedding_model=embedding_model
        )

        self.scoring_engine = ScoringEngine()

        self.perspective_orchestrator = PerspectiveOrchestrator()

        # --------------------------------------------------
        # Context & Prompt
        # --------------------------------------------------

        self.context_builder = ContextBuilder()
        self.prompt_builder = PromptBuilder()

        # --------------------------------------------------
        # Query Pipeline
        # --------------------------------------------------

        self.pipeline = QueryPipeline(
            intent_engine=self.intent_engine,
            role_engine=self.role_engine,
            retrieval_engine=self.retrieval_engine,
            scoring_engine=self.scoring_engine,
            perspective_orchestrator=self.perspective_orchestrator,
            context_builder=self.context_builder,
            prompt_builder=self.prompt_builder,
            llm_client=llm_client,
            log_path=log_path
        )

    def query(self, query: str):
        """
        Execute a query through the full knowledge engine.

        Returns:
            QueryContext containing the full execution trace.
        """

        return self.pipeline.run(query)


# --------------------------------------------------
# Example Usage (for testing)
# --------------------------------------------------

if __name__ == "__main__":

    # Dummy placeholders (replace with real implementations)
    knowledge_base = None
    embedding_model = None
    llm_client = None

    engine = KnowledgeEngine(
        knowledge_base=knowledge_base,
        embedding_model=embedding_model,
        llm_client=llm_client
    )

    result = engine.query("What does DORA require for cloud outsourcing?")

    print(result)
