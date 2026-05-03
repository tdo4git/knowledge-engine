# Retrieval Architecture Guideline -- Strategic Knowledge Engine

## 1. Purpose

The Retrieval Engine is responsible for transforming a user query into a
high‑quality knowledge context for downstream reasoning.

------------------------------------------------------------------------

# 2. Retrieval Pipeline

query → intent detection → role detection → query embedding → vector
search → scoring → document grouping → context construction

------------------------------------------------------------------------

# 3. Step 1 -- Intent Detection

Module: intent_engine.py

Identifies the purpose of the query.

Examples:

analysis explanation comparison summary recommendation

Intent affects ranking and context generation.

------------------------------------------------------------------------

# 4. Step 2 -- Role Detection

Module: role_engine.py

Determines the perspective of the user.

Examples:

trusted advisor insurance expert cloud architect regulatory analyst

Role determines which knowledge domains receive higher weight.

------------------------------------------------------------------------

# 5. Step 3 -- Query Embedding

The query is embedded using the same embedding model used for document
chunks.

Example model:

sentence-transformers/all-MiniLM-L6-v2

------------------------------------------------------------------------

# 6. Step 4 -- Vector Search

The query embedding is compared against the FAISS index.

Search returns:

Top-K most similar chunks.

------------------------------------------------------------------------

# 7. Step 5 -- Scoring

Similarity scores are adjusted using metadata signals:

knowledge_domain weight origin reliability document_type importance
recency (optional)

------------------------------------------------------------------------

# 8. Step 6 -- Document Grouping

Relevant chunks belonging to the same document are grouped.

Purpose:

avoid fragmented answers build coherent context

------------------------------------------------------------------------

# 9. Step 7 -- Context Construction

The highest ranked chunks are assembled into a context window for the
reasoning model.

Context includes:

chunk text document metadata source references

------------------------------------------------------------------------

# 10. Design Principles

Retrieval must be:

Explainable Deterministic where possible Metadata-aware Efficient

------------------------------------------------------------------------

# 11. Integration with Knowledge Base

Retrieval reads from:

vector_index/index.faiss chunks/chunks.json
registry/document_registry.json

------------------------------------------------------------------------

# 12. Future Extensions

Hybrid search (vector + keyword)

Reranking models

Adaptive scoring

Cross-document synthesis
