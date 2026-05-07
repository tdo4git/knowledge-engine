import argparse
from pathlib import Path

from config.construction_config import EMBEDDING_MODEL

BASE_PATH = Path(__file__).resolve().parent.parent

(BASE_PATH / "knowledge_base" / "audit").mkdir(parents=True, exist_ok=True)

from knowledge_core.pipeline.query_pipeline import QueryPipeline
from knowledge_core.retrieval.retrieval_engine import RetrievalEngine
from knowledge_core.scoring.scoring_engine import ScoringEngine
from knowledge_core.perspectives.perspective_orchestrator import PerspectiveOrchestrator
from knowledge_core.pipeline.context_builder import ContextBuilder
from knowledge_core.prompt.prompt_governance import PromptBuilder
from knowledge_core.intent.intent_engine import detect_intent
from knowledge_core.roles.role_engine import RoleEngine
from knowledge_base.knowledge_base import KnowledgeBase
from sentence_transformers import SentenceTransformer


class _NoLLM:
    def generate(self, prompt: str) -> str:
        return "[RETRIEVAL-ONLY MODE — LLM skipped]"


class _IntentAdapter:
    def detect_intent(self, query):
        return detect_intent(query)


def run_query(query: str, retrieval_only: bool = False):

    import os
    os.chdir(BASE_PATH)

    kb    = KnowledgeBase.load_from_disk("knowledge_base")
    model = SentenceTransformer(EMBEDDING_MODEL)

    if retrieval_only:
        llm_client = _NoLLM()
    else:
        from knowledge_core.llm.llm_client import LLMClient
        llm_client = LLMClient()

    pipeline = QueryPipeline(
        intent_engine=_IntentAdapter(),
        role_engine=RoleEngine(),
        retrieval_engine=RetrievalEngine(knowledge_base=kb, embedding_model=model),
        scoring_engine=ScoringEngine(),
        perspective_orchestrator=PerspectiveOrchestrator(),
        context_builder=ContextBuilder(),
        prompt_builder=PromptBuilder(),
        llm_client=llm_client,
        log_path="knowledge_base/audit/query_audit_log.jsonl"
    )

    ctx = pipeline.run(query)

    print("\n" + "=" * 60)
    print("QUERY")
    print("=" * 60)
    print(ctx.query)

    print("\n=== INTENT ===")
    print(ctx.intent)

    print("\n=== ROLE ===")
    print(ctx.role)

    print("\n=== RAW CHUNKS — Top 10 (by similarity) ===")
    for c in ctx.retrieval_result.chunk_candidates[:10]:
        print(f"  {round(c.similarity_score, 4)}  {c.chunk_id}  ({c.doc_id})")

    print("\n=== RANKED DOCUMENTS (after scoring) ===")
    for d in ctx.ranked_documents:
        print(f"  score={round(d.score, 4)}  "
              f"semantic={round(d.semantic_score, 4)}  "
              f"governance={round(d.governance_score, 4)}  "
              f"{d.doc_id}")

    print("\n=== CONTEXT CHUNKS (selected for LLM) ===")
    for c in ctx.context_package.chunks:
        print(f"\n  [{c.doc_id} | {c.chunk_id}]")
        print(f"  {c.text[:600].strip()}")

    print("\n=== RESPONSE ===")
    print(ctx.response)

    print("\n=== DIAGNOSTICS ===")
    print(f"  chunk_candidates : {len(ctx.retrieval_result.chunk_candidates)}")
    print(f"  ranked_documents : {len(ctx.ranked_documents)}")
    print(f"  context_chunks   : {len(ctx.context_package.chunks)}")
    print(f"  sources          : {ctx.context_package.sources}")
    print(f"  embedding_model  : {EMBEDDING_MODEL}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Run a query through the Knowledge Engine")
    parser.add_argument("query", help="The query string")
    parser.add_argument(
        "--retrieval-only",
        action="store_true",
        help="Skip LLM — validate retrieval pipeline only"
    )
    args = parser.parse_args()
    run_query(args.query, retrieval_only=args.retrieval_only)


if __name__ == "__main__":
    main()