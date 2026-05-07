from knowledge_core.pipeline.query_context import QueryContext
from knowledge_core.audit.retrieval_decision_log import RetrievalDecisionLogger


class QueryPipeline:

    def __init__(
        self,
        intent_engine,
        role_engine,
        retrieval_engine,
        scoring_engine,
        perspective_orchestrator,
        context_builder,
        prompt_builder,
        llm_client,
        log_path
    ):

        self.intent_engine = intent_engine
        self.role_engine = role_engine

        self.retrieval_engine = retrieval_engine
        self.scoring_engine = scoring_engine

        self.perspective_orchestrator = perspective_orchestrator

        self.context_builder = context_builder
        self.prompt_builder = prompt_builder

        self.llm_client = llm_client

        self.logger = RetrievalDecisionLogger(log_path)

    def run(self, query):

        # --------------------------------------------------
        # Initialize Query Context
        # --------------------------------------------------

        ctx = QueryContext(query=query)

        # --------------------------------------------------
        # 1 Intent Detection
        # --------------------------------------------------

        ctx.intent = self.intent_engine.detect_intent(ctx.query)

        # --------------------------------------------------
        # 2 Role Detection
        # --------------------------------------------------

        ctx.role = self.role_engine.detect_role(ctx.intent)

        # --------------------------------------------------
        # 3 Retrieval
        # --------------------------------------------------

        ctx.retrieval_result = self.retrieval_engine.retrieve(ctx.query)

        # --------------------------------------------------
        # 4 Document Scoring
        # --------------------------------------------------

        ctx.ranked_documents = self.scoring_engine.score(
            ctx.retrieval_result.document_candidates
        )

        # --------------------------------------------------
        # 5 Flatten documents → chunks (mit Score-Propagation)
        # --------------------------------------------------

        scored_chunks = []
        for doc in ctx.ranked_documents:
            for chunk in doc.chunks:
                chunk.score = doc.score
                scored_chunks.append(chunk)

        # --------------------------------------------------
        # 6 Score-basierte Selektion
        #
        # PerspectiveOrchestrator deaktiviert — die
        # ScoringEngine liefert bereits governance-aware
        # Ranking. Erzwungene Perspektiv-Quoten würden
        # schwache Chunks in den Context ziehen.
        # Reaktivierung sinnvoll wenn Knowledge Base
        # pro Perspektive ausreichend starke Dokumente hat.
        # --------------------------------------------------

        max_chunks = (
            ctx.context_package is None and
            10 or len(ctx.context_package.chunks)
        )

        selected_chunks = scored_chunks[:10]

        # --------------------------------------------------
        # 7 Context Construction
        # --------------------------------------------------

        ctx.context_package = self.context_builder.build_context(
            query=ctx.query,
            chunks=selected_chunks
        )

        # --------------------------------------------------
        # 8 Retrieval Decision Log
        # --------------------------------------------------

        try:
            self.logger.log(
                query=ctx.query,
                intent=ctx.intent,
                role=ctx.role,
                ranked_documents=ctx.ranked_documents,
                context_package=ctx.context_package
            )
        except Exception as e:
            print("Retrieval audit logging failed:", e)

        # --------------------------------------------------
        # 9 Prompt Generation
        # --------------------------------------------------

        ctx.prompt = self.prompt_builder.build_prompt(
            query=ctx.query,
            role=ctx.role,
            perspective=ctx.intent.content_intent,
            context_package=ctx.context_package
        )

        # --------------------------------------------------
        # 10 LLM Execution
        # --------------------------------------------------

        ctx.response = self.llm_client.generate(ctx.prompt)

        return ctx