import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.makedirs("logs", exist_ok=True)

from config.construction_config import EMBEDDING_MODEL

from knowledge_core.pipeline.query_pipeline import QueryPipeline
from knowledge_core.retrieval.retrieval_engine import RetrievalEngine
from knowledge_core.scoring.scoring_engine import ScoringEngine
from knowledge_core.perspectives.perspective_orchestrator import PerspectiveOrchestrator
from knowledge_core.pipeline.context_builder import ContextBuilder
from knowledge_core.prompt.prompt_governance import PromptBuilder
from knowledge_core.intent.intent_engine import detect_intent
from knowledge_core.roles.role_engine import RoleEngine
from knowledge_base.knowledge_base import KnowledgeBase
from knowledge_core.llm.llm_client import LLMClient
from sentence_transformers import SentenceTransformer


class IntentEngineAdapter:
    def detect_intent(self, query):
        return detect_intent(query)


def run_test(query: str):

    print("\n==============================")
    print("QUERY")
    print("==============================")
    print(query)

    kb    = KnowledgeBase.load_from_disk("knowledge_base")
    model = SentenceTransformer(EMBEDDING_MODEL)

    pipeline = QueryPipeline(
        intent_engine=IntentEngineAdapter(),
        role_engine=RoleEngine(),
        retrieval_engine=RetrievalEngine(knowledge_base=kb, embedding_model=model),
        scoring_engine=ScoringEngine(),
        perspective_orchestrator=PerspectiveOrchestrator(),
        context_builder=ContextBuilder(),
        prompt_builder=PromptBuilder(),
        llm_client=LLMClient(),
        log_path="logs/retrieval_log.jsonl"
    )

    ctx = pipeline.run(query)

    print("\n=== INTENT ===")
    print(ctx.intent)

    print("\n=== ROLE ===")
    print(ctx.role)

    print("\n=== RAW CHUNKS (Top 5) ===")
    for c in ctx.retrieval_result.chunk_candidates[:5]:
        print({
            "chunk_id": c.chunk_id,
            "doc_id":   c.doc_id,
            "similarity": round(c.similarity_score, 4)
        })

    print("\n=== RANKED DOCUMENTS ===")
    for d in ctx.ranked_documents:
        print({
            "doc_id":   d.doc_id,
            "score":    round(d.score, 4),
            "semantic": round(d.semantic_score, 4),
            "governance": round(d.governance_score, 4)
        })

    print("\n=== CONTEXT ===")
    for c in ctx.context_package.chunks:
        print({
            "doc_id": c.doc_id,
            "text":   c.text[:150]
        })

    print("\n=== RESPONSE ===")
    print(ctx.response)

    print("\n=== DIAGNOSTICS ===")
    print({
        "chunks":          len(ctx.retrieval_result.chunk_candidates),
        "documents":       len(ctx.ranked_documents),
        "context_chunks":  len(ctx.context_package.chunks),
        "embedding_model": EMBEDDING_MODEL
    })


if __name__ == "__main__":
    run_test("Was fordert DORA hinsichtlich Cloud-Auslagerung bei Versicherungen?")