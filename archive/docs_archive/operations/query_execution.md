# Query Execution – Operational Guide
Version: 1.0
Layer: Operations

## Ziel

Dieses Dokument definiert die operative Nutzung der Strategic Knowledge Engine.

Es beschreibt:
- den Einstiegspunkt
- den tatsächlichen Laufzeitfluss
- die Teststrategie

---

# 1. Entry Point

Zentraler Einstiegspunkt für jede Query:

QueryPipeline.run(query)

Die QueryPipeline ist die einzige erlaubte Orchestrierungsschicht für produktive Nutzung.

---

# 2. Pipeline Flow (Runtime)

Die Engine verarbeitet jede Query deterministisch entlang folgender Schritte:

1. Intent Detection
2. Role Detection
3. Retrieval Engine
4. Scoring Engine (Governance)
5. Perspective Orchestrator
6. Context Builder
7. Prompt Governance
8. LLM Execution

Datenobjekt:
→ QueryContext (trägt gesamten Zustand)

---

# 3. Komponenten-Verantwortung

## Retrieval Engine
- liefert Chunk Candidates
- aggregiert zu Document Candidates
- KEIN finales Ranking

## Scoring Engine
- wendet Governance-Regeln an
- erzeugt finales Ranking

## Context Builder
- selektiert:
  - max_documents
  - max_chunks_per_document
- baut LLM Context

## Prompt Governance
- erzwingt:
  - Rollenverhalten
  - Quellenrestriktion
  - keine Halluzination

---

# 4. Teststrategie

## Level 1 – Retrieval Test (Debug)

Ziel:
- Embedding korrekt?
- FAISS Retrieval korrekt?
- Aggregation sinnvoll?

Entry:
→ RetrievalEngine.retrieve()

Output:
- chunk_candidates
- document_candidates

Nicht getestet:
- Governance
- finaler Context

---

## Level 2 – Pipeline Test (Standard)

Ziel:
- Ranking korrekt?
- Governance greift?
- Context sinnvoll?

Entry:
→ QueryPipeline.run()

Output:
- ranked_documents
- context_package
- prompt
- response (Dummy LLM möglich)

---

## Level 3 – End-to-End Test

Ziel:
- reale Antwortqualität
- Prompt + Context Wirkung

Entry:
→ QueryPipeline.run() + echtes LLM

---

# 5. Debugging-Regeln

Bei Fehlern:

1. Retrieval falsch?
→ Level 1 prüfen

2. Ranking falsch?
→ Scoring Engine prüfen

3. Context schlecht?
→ Context Builder prüfen

4. Halluzination?
→ Prompt Governance prüfen

---

# 6. Pflichtanforderungen (Non-Negotiable)

Jeder Test muss sichtbar machen:

- doc_id
- chunk_id
- Scores
- Ranking-Reihenfolge

Sonst:
→ kein Explainability-konformes System

---

# 7. Anti-Patterns (vermeiden)

❌ direkte Nutzung der Retrieval Engine für Antworten  
❌ LLM ohne Context Builder  
❌ Scoring außerhalb der zentralen Pipeline  
❌ fehlende Traceability  

---

# Fazit

Die QueryPipeline ist:

→ der einzige valide Einstiegspunkt  
→ die zentrale Steuerung der Engine  
→ die Basis für alle Tests > Level 1