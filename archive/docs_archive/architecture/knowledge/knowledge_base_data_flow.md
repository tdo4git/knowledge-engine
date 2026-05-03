# Knowledge Base Data Flow

Strategic Knowledge Engine -- Architecture Layer

This document describes the data flow within the Knowledge Construction
Pipeline and the resulting Knowledge Base artifacts used by the
Retrieval Engine.

The goal is to make the transformation from documents to retrieval‑ready
knowledge fully transparent and explainable.

------------------------------------------------------------------------

# 1. Data Flow Overview

Document Sources ↓ Knowledge Construction Pipeline ↓ Knowledge Base ↓
Knowledge Engine Retrieval

------------------------------------------------------------------------

# 2. Detailed Data Flow

``` mermaid
flowchart LR

subgraph Sources["Document Sources"]
A[intake]
B[archive]
end

subgraph Construction["Knowledge Construction"]
C[Preview Extractor]
D[Document Classifier]
E[Governance Pipeline]
F[Validation]
G[Registry Builder]
H[Document Text Extractor]
I[Chunker]
J[Embedding Generator]
K[Index Consistency Check]
end

subgraph KnowledgeBase["Knowledge Base"]
L[Document Registry]
M[Chunks]
N[Embeddings]
O[FAISS Index]
P[Audit Log]
end

A --> B

B --> C
C --> D
D --> E
E --> F
F --> G

G --> L

B --> H
H --> I
I --> M

M --> J
J --> N
N --> O

J --> K

F --> P
```

------------------------------------------------------------------------

# 3. Knowledge Base Artifacts

The Knowledge Construction pipeline generates the following artifacts:

knowledge_base/

registry/ document_registry.json

chunks/ chunks.json

vector_index/ embeddings.pt index.faiss

audit/ onboarding_audit_log.jsonl

These artifacts together form the **Knowledge Base** used by the engine.

------------------------------------------------------------------------

# 4. Artifact Relationships

The artifacts have a strict structural relationship:

Document Registry ↓ doc_id Chunks ↓ index alignment Embeddings ↓ vector
mapping Vector Index

Each chunk references a document via `doc_id`. Embeddings correspond to
the chunk order. The FAISS index is built from the embedding matrix.

------------------------------------------------------------------------

# 5. Retrieval Consumption

The Retrieval Engine reads the following artifacts:

vector_index/index.faiss chunks/chunks.json
registry/document_registry.json

Retrieval Flow:

Query → Candidate Chunk Retrieval → Document Grouping → Governance
Scoring → Context Construction → LLM Response

------------------------------------------------------------------------

# 6. Design Principles

Deterministic Structure\
Artifacts are generated exclusively by the Knowledge Construction
pipeline.

Immutable Runtime Data\
The Knowledge Base is treated as read‑only during runtime.

Explainability\
Every retrieved chunk can be traced back to its source document.

Governance\
Registry metadata controls retrieval weighting and trust levels.

------------------------------------------------------------------------

# 7. Responsibility Separation

Knowledge Construction → write access\
Knowledge Engine → read access\
Bots → read access

This separation ensures consistency, traceability, and governance.
