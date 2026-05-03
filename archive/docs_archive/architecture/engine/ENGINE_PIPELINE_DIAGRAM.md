# Knowledge Engine -- Query Pipeline Diagram

This diagram shows how a user query flows through the Knowledge Engine.

``` mermaid
flowchart LR

    A[User Query]

    B[Intent Engine]
    C[Role Engine]
    D[Retrieval Engine]
    E[Scoring Engine]
    F[Context Builder]
    G[Perspective Orchestrator]
    H[Prompt Governance]
    I[LLM]
    J[Final Answer]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I

    Query
    → Intent Engine
    → Role Engine
    → Retrieval Engine
    → Scoring Engine
    → Context Builder
    → Perspective Orchestrator
    → Prompt Governance
    → LLM
```
