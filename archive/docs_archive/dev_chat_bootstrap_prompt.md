# Projektkontext – Strategic Knowledge Engine

Ich entwickle eine **Strategic Knowledge Engine** für einen erklärbaren Knowledge Bot im Versicherungs- und Consulting-Kontext.

Der Chat soll mir helfen, die **Retrieval Engine zu implementieren**, basierend auf der bereits implementierten Knowledge Construction Pipeline.

Bitte arbeite strukturiert, architekturorientiert und entwicklungsnah.

---

# Aktueller Projektstatus

Die **Knowledge Construction Pipeline ist vollständig implementiert**.

Sie erzeugt eine strukturierte Knowledge Base aus Dokumenten.

Pipeline:

document
→ preview extraction
→ document classification (LLM)
→ governance rules
→ validation
→ registry entry
→ text extraction
→ token-based chunking
→ incremental embedding generation
→ FAISS vector index
→ consistency check
→ audit log

Die Pipeline läuft automatisiert über eine **OnboardingPipeline**.

---

# Knowledge Base Struktur

knowledge_base/

registry/
document_registry.json

chunks/
chunks.json

vector_index/
embeddings.pt
chunk_ids.json
index.faiss

audit/
onboarding_audit_log.jsonl

Die Knowledge Base wird ausschließlich durch die Construction Pipeline erzeugt und ist zur Laufzeit **read-only**.

---

# Architektur der Strategic Knowledge Engine

Document Sources
→ Knowledge Construction
→ Knowledge Base
→ Knowledge Engine
→ Bots

Engine-Pipeline:

Query
→ Intent Engine
→ Role Engine
→ Retrieval Engine
→ Scoring Engine
→ Perspective Orchestrator
→ Prompt Governance
→ LLM
→ Answer

Die Module **Intent Engine** und **Role Engine** sind bereits implementiert.

---

# Implementierte Code-Struktur

knowledge-engine/

knowledge_core/

intent/
role/
retrieval/
scoring/
perspective/
prompt/
pipeline/

knowledge_construction/

metadata/
validation/
governance/
registry/
chunking/
embedding/
document_processing/
onboarding_pipeline.py

knowledge_base/

registry/
chunks/
vector_index/

bots/

trusted_advisor_bot
marketing_bot
insurance_portfolio_bot

---

# Architekturprinzipien

Die Engine folgt mehreren zentralen Prinzipien:

1. Separation of Concerns
   Knowledge Construction und Retrieval sind strikt getrennt.

2. Explainability
   Jede Antwort muss auf Dokumente und Chunks zurückführbar sein.

3. Governance
   Regulatorische Quellen haben Vorrang vor Advisory- oder Marketing-Quellen.

4. LLM Role
   Das LLM erzeugt keine neuen Fakten, sondern formuliert nur auf Basis der Retrieval-Ergebnisse.

---

# Dokumentationsstruktur

docs/

meta/
governance/
architecture/
evolution/
scope/
strategy/

Wichtige Architektur-Dokumente:

* system_overview.md
* architecture_overview_v3.md
* knowledge_construction_pipeline.md
* knowledge_base_schema.md
* knowledge_base_data_flow.md
* retrieval_architecture_guideline.md
* explainability_principles.md

---

# Aktuelles Entwicklungsziel

Ich möchte jetzt die **Retrieval Engine implementieren**.

Die Retrieval-Pipeline soll enthalten:

query
→ query embedding
→ vector search
→ candidate chunks
→ metadata scoring
→ document grouping
→ context construction

Die nächsten Architekturentscheidungen betreffen:

* Candidate Retrieval Strategy
* Top-K Auswahl
* Metadata-Scoring
* Document-centric Ranking
* Context Window Construction

---

# Aufgabe für diesen Chat

Hilf mir bei der **sauberen Implementierung der Retrieval Engine**.

Arbeite dabei:

* architekturorientiert
* modular
* kompatibel mit der bestehenden Engine-Struktur
* kompatibel mit der bestehenden Knowledge Base

Wir beginnen mit der **Candidate Retrieval Strategie**.
