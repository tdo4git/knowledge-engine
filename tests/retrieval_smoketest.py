from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np
from pathlib import Path
from collections import defaultdict

from config.construction_config import EMBEDDING_MODEL

BASE_DIR = Path(__file__).resolve().parents[1]

index_path  = BASE_DIR / "knowledge_base/vector_index/index.faiss"
chunks_path = BASE_DIR / "knowledge_base/chunks/chunks.json"

print("BASE_DIR:   ", BASE_DIR)
print("Index Path: ", index_path)
print("Chunks Path:", chunks_path)
print("Model:      ", EMBEDDING_MODEL)

if not index_path.exists():
    raise FileNotFoundError(f"Index not found: {index_path}")
if not chunks_path.exists():
    raise FileNotFoundError(f"Chunks not found: {chunks_path}")

index = faiss.read_index(str(index_path))

with open(chunks_path) as f:
    chunks = json.load(f)

model = SentenceTransformer(EMBEDDING_MODEL)

query  = "Was fordert DORA hinsichtlich Cloud-Auslagerung bei Versicherungen?"
q_emb  = model.encode([query])

k = min(20, index.ntotal)
D, I = index.search(q_emb, k=k)

doc_scores = defaultdict(list)

for score, idx in zip(D[0], I[0]):
    chunk = chunks[idx]
    doc_scores[chunk["doc_id"]].append(score)

doc_ranking = []

for doc_id, scores in doc_scores.items():
    top_scores = sorted(scores)[:3]
    agg_score  = np.mean(top_scores)
    doc_ranking.append((doc_id, agg_score))

doc_ranking = sorted(doc_ranking, key=lambda x: x[1])

print("\n--- INDEX INFO ---")
print(f"ntotal: {index.ntotal}")
print(f"dim:    {index.d}")

print("\n--- DOCUMENT RANKING ---\n")
for doc_id, score in doc_ranking:
    print(f"{score:.4f}  {doc_id}")