# Architectural Principles

Separation of Concerns

Knowledge construction and knowledge retrieval are strictly separated.

Explainability

Every answer can be traced to the underlying documents.

Governance

Registry metadata influences ranking and trust levels.

Document-centric Retrieval

Documents, not isolated chunks, form the basis of reasoning contexts.

---

# 🔥 NEW: End-to-End Explainability

Explainability spans both system layers:

## Construction Phase

- metadata classification decisions are explainable
- governance rules provide traceable outputs
- registry entries can be audited

## Retrieval Phase

- document selection is explainable
- scoring decisions are transparent
- context construction is traceable

End-to-end traceability:

document → registry → chunk → retrieval → answer

This ensures full transparency across the system lifecycle.