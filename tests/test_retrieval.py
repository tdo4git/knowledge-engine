# test_retrieval.py
from pathlib import Path

from knowledge_core.retrieval.retrieval_engine import RetrievalEngine

def run_test(query: str):
    engine = RetrievalEngine()

    result = engine.retrieve(query)

    print("\n=== QUERY ===")
    print(query)

    print("\n=== DOCUMENTS ===")
    for doc in result.documents:
        print({
            "doc_id": doc.doc_id,
            "score": doc.score,
            "origin": doc.metadata.get("origin"),
            "type": doc.metadata.get("document_type")
        })

    print("\n=== CHUNKS ===")
    for chunk in result.chunks:
        print({
            "chunk_id": chunk.chunk_id,
            "doc_id": chunk.doc_id,
            "score": chunk.score,
            "text": chunk.text[:200]
        })

if __name__ == "__main__":
    run_test("Was fordert DORA hinsichtlich Cloud-Auslagerung bei Versicherungen?")