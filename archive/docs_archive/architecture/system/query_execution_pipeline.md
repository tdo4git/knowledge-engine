Query Execution Pipeline

The Query Execution Pipeline orchestrates the runtime behaviour of the
Strategic Knowledge Engine.

Pipeline

Query
→ Intent Engine
→ Role Engine
→ Retrieval Engine
→ Scoring Engine
→ Perspective Orchestrator
→ Context Builder
→ Prompt Governance
→ LLM
→ Answer

The QueryContext object captures the full execution state of a query.

It stores all intermediate results produced during query processing,
including retrieval results, document ranking, and the generated prompt.

This structure enables:

- debugging
- explainability
- audit logging
- evaluation

## LLM Interaction Model (Updated)

LLM interaction is fully contract-driven:

- Contracts (YAML) define behavior and rules
- Prompt Builder translates contracts into prompts
- LLMClient executes requests (no embedded logic)

Separation of concerns:

Contract → Prompt Builder → LLMClient

RULE:
- No prompt logic inside LLMClient
- No hardcoded prompts
- All prompts must be contract-driven


## Prompt Construction (Update)

Prompt generation is contract-driven:

- Retrieval provides structured context
- Prompt Builder applies task-specific contracts
- LLMClient executes without embedded logic

Retrieval does not generate prompts directly.
It only provides structured, ranked context.