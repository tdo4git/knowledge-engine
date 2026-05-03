# Explainability & Trust Principles

## 1. Quellenpriorisierung
- Regulatorische Dokumente haben Vorrang vor Advisory-Quellen.
- Advisory-Quellen dienen ausschließlich der Einordnung.

## 2. Rollenmodell
- Dokumente sind fachlichen Rollen zugeordnet (z. B. regulatorisch, advisor).
- Das Rollenmodell steuert Retrieval und Gewichtung.

## 3. LLM-Nutzung
- Das LLM generiert keine neuen Fakten.
- Es formuliert ausschließlich auf Basis vorselektierter Inhalte.

## 4. Transparenz
- Jede Antwort kann in ihrer Entstehung erklärt werden (C1).
- Die Systemarchitektur ist nachvollziehbar dokumentiert (C2).

## 5. Grenzen
- Kein Ersatz für Rechtsberatung.
- Kein Anspruch auf Vollständigkeit.
- Fokus auf kuratierte Inhalte.

---

## Governance Execution Model (Update)

All governance rules are executed via a centralized pipeline:

apply_governance()

This ensures:
- deterministic behavior
- traceability
- no duplicated logic

Derived attributes:
- bias
- confidence

RULE:
Governance must not be implemented outside the central pipeline.

---

## Retrieval Explainability (Update)

Explainability includes:

- which documents were retrieved
- how they were ranked (scoring signals)
- which chunks were selected

This is enabled by:

- document-centric retrieval
- governance-aware scoring
- QueryContext tracking

Every answer can be traced back to:
doc_id → chunk_id → registry metadata → scoring decision

---

# 🔥 NEW: Governance Explainability Layer (V1)

Explainability is extended to the **knowledge construction phase**.

For every derived metadata field (e.g. origin, document_type, knowledge_domain),
the system must provide a traceable explanation.

## Explainability Requirements

For each field, the system captures:

- **applied_rule**  
  → which governance rule determined the value

- **signal**  
  → which keyword / mapping / condition triggered the rule

- **source**  
  → decision source (e.g. preview_rule, filename_rule, rule_based, llm)

## Example

```json
{
  "origin": "consulting_firm",
  "origin_explain": {
    "applied_rule": "AUTHOR_ORIGIN_MAP",
    "signal": "exxeta",
    "source": "preview_rule"
  }
}