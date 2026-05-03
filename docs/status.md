# Status – Strategic Knowledge Engine
Zuletzt aktualisiert: 2026-05-03

---

## Projektstand

### Abgeschlossen

**Knowledge Construction Pipeline** — vollständig implementiert und getestet.
- LLM-basierte Klassifikation (YAML contract-driven)
- Governance Rules (zentralisiert, deterministisch)
- Validation (Enum + Cross-Field)
- Registry, Chunking, Embedding, FAISS Index
- Audit Logging
- Onboarding-Validierung mit Expectation-Framework

**Knowledge Engine (Query-Seite)** — architektonisch vollständig, implementiert.
- Intent Engine
- Role Engine
- Retrieval Engine (FAISS vector search, Document Aggregation)
- Scoring Engine (Governance-aware Ranking)
- Context Builder
- Perspective Orchestrator
- Prompt Governance
- QueryPipeline (End-to-End lauffähig)

**Claude API Integration** — abgeschlossen (2026-05-01)
- `knowledge_construction/llm/llm_client.py` auf Anthropic API umgestellt
- `knowledge_core/llm/llm_client.py` neu erstellt (Query Pipeline)
- `config/construction_config.py`: LLM_MODEL = claude-sonnet-4-6
- Retrieval Audit Logger: JSON-Serialisierung für Dataclasses gefixt
- End-to-End Test erfolgreich: Construction + Query Pipeline mit echtem Claude

**Onboarding Stabilisierung** — abgeschlossen (2026-05-03)
- TD-001: Doc-Hash Duplicate Check wiederhergestellt
- TD-002: Doc-ID Schema verbessert (`doc_{origin}_{topic}_{year?}_{hash6}`)
- TD-003: Review-Flow formalisiert — Validation blockiert, Review-Report automatisch
- TD-006: Bias-Logik korrigiert, `corporate` als neue Origin-Kategorie
- Governance-Keyword-Probleme behoben (`ey`, `msg`, `insur` Substring-Matches)
- Archivierung implementiert: intake/ → archive/ nach erfolgreichem Onboarding
- LLM-Domain-Normalisierung: Topic-Werte auf gültige KNOWLEDGE_DOMAINS gemappt

**Knowledge Base** — 6 Dokumente, sauber klassifiziert (2026-05-03)
- `doc_bafin_cloud_2024_53f735` — BaFin Cloud Outsourcing 2024
- `doc_eu_dora_2024_d54141` — Exxeta DORA Practical Guide 2024
- `doc_aws_sovereignty_1c18e9` — AWS Digital Sovereignty Framework
- `doc_unknown_allianz_6ae771` — Allianz Tech-Konzern Blog
- `doc_eu_dora_2022_0eb896` — DORA Verordnung EU 2022
- `doc_aws_cloud_95e9f7` — AWS Insurance on the Cloud

**Dokumentation** — vollständig überarbeitet und konsolidiert (Mai 2026)
- architecture.md
- status.md
- decisions.md
- technical_debt.md

---

### Offen / Nächste Schritte

**Priorität 1 — Knowledge Base befüllen**
- Aktuell 6 Dokumente — Ziel: 15–20 echte Dokumente
- Dokumenttypen: regulatorisch, Whitepaper, interne Dokumente, Beratungsframeworks
- Onboarding-Pipeline ist stabil und bereit

**Priorität 2 — Trusted Advisor Bot**
- `bots/trusted_advisor_bot/` implementieren
- Primärer Use Case: Berater-Bot für Versicherungs-Consulting
- Voraussetzung: ausreichend Dokumente in Knowledge Base

**Priorität 3 — Weitere technische Schulden**
- TD-005: Topic als Klassifikationsdimension
- TD-009: AUTHOR_ORIGIN_MAP Keyword-Qualität (Wort-Grenz-Matching)
- TD-010: Doc-ID Origin aus Governance statt LLM
- TD-004: Regressionstest auf Referenzdokumente begrenzen
- TD-007: Reklassifizierungs-Skript
- TD-008: Ingestion-Layer Web-Quellen

---

## Technischer Stack

| Komponente | Technologie |
|---|---|
| Sprache | Python |
| IDE | VS Code |
| Laufzeit | lokal, MacBook |
| Embedding | sentence-transformers/all-MiniLM-L6-v2 |
| Vektorindex | FAISS |
| LLM (Construction) | Claude claude-sonnet-4-6 (Anthropic API) |
| LLM (Query) | Claude claude-sonnet-4-6 (Anthropic API) |

---

## Bekannte Schwächen

- 6 Dokumente in der Knowledge Base → Retrieval noch nicht aussagekräftig
- Doc-ID enthält Origin aus LLM-Klassifikation, nicht aus Governance (TD-010, kosmetisch)
- Kein Bot implementiert
- Kein Ingestion-Layer für Web-Quellen
- AUTHOR_ORIGIN_MAP verwendet Substring-Matching → potenzielle False Positives (TD-009)
