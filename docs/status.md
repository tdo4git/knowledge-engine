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

**Governance & Klassifikation** — stabilisiert (2026-05-03)
- Origin-Detection auf Titel + Dateiname beschränkt (kein Preview-Text) → verhindert False Positives durch regulatorischen Inhalt
- Classifier-Truncation entfernt: Preview-Größe ausschließlich über `PREVIEW_MAX_CHARS` in `construction_config.py` gesteuert
- `supervisory_authority` → Prefix `doc_supervisory_*` statt `doc_bafin_*`
- `corporate` in `_normalize_origin` ergänzt → `doc_corporate_*` korrekt
- OECD von `supervisory_authority` auf `research_institution` korrigiert
- `AUTHOR_ORIGIN_MAP` und `FILENAME_KEYWORDS` deutlich erweitert (Capgemini, BearingPoint, Lünendonk, Trendzowl, heise, amber, Beltios, R+V, adesso u.a.)
- TD-010 implizit gelöst: `generate_doc_id()` läuft nach Governance, verwendet finale Origin

**Knowledge Base** — 25 Dokumente, sauber klassifiziert, 0 Review-Punkte (2026-05-03)

| Doc-ID | Dokument | Origin |
|---|---|---|
| `doc_supervisory_cloud_2024_53f735` | BaFin Cloud Outsourcing 2024 | supervisory_authority |
| `doc_supervisory_insurance_83c73b` | EIOPA Digitalisation Report | supervisory_authority |
| `doc_supervisory_cloud_a51b3a` | EIOPA Cloud & AI Future | supervisory_authority |
| `doc_supervisory_stellungnahmemenschundmaschinekurzfassung_6ba9b6` | Stellungnahme Mensch & Maschine | supervisory_authority |
| `doc_supervisory_20250903versicherungsmarktbericht2024_2025_10cbfd` | BaFin Versicherungsmarktbericht 2024 | supervisory_authority |
| `doc_eu_dora_2022_0eb896` | DORA Verordnung EU 2022 | legislator |
| `doc_consulting_dora_2024_d54141` | Exxeta DORA Practical Guide | consulting_firm |
| `doc_consulting_playbookbearingpointversicherung2030_2030_717627` | BearingPoint Playbook Versicherung 2030 | consulting_firm |
| `doc_consulting_insurance_2024_19f71c` | Capgemini P&C Top Trends 2024 | consulting_firm |
| `doc_consulting_insurance_2030_131197` | Claims 2030 Talent Strategy | consulting_firm |
| `doc_consulting_dora_2024_d54141` | Exxeta DORA Practical Guide 2024 | consulting_firm |
| `doc_consulting_sind_2026_0b05a4` | IT-Trends 2026 | consulting_firm |
| `doc_research_insurance_2025_abeb26` | Global Insurance Report 2025 | research_institution |
| `doc_research_insurance_2025_1ebdd0` | OECD Global Insurance Market Trends 2025 | research_institution |
| `doc_research_insurance_2a0a0c` | Lünendonk Digital Outlook Insurance | research_institution |
| `doc_research_elingassekuranz20302_2030_3862f3` | Eling Assekuranz 2030 | research_institution |
| `doc_research_insurance_2025_588dcd` | Trendzowl Insurance Trends 2025 | research_institution |
| `doc_aws_sovereignty_1c18e9` | AWS Digital Sovereignty Framework | cloud_vendor |
| `doc_aws_cloud_95e9f7` | AWS Insurance on the Cloud | cloud_vendor |
| `doc_vendor_heiseacademymycompany_6d0ccf` | HeiseAcademy MyCompany GPT | software_vendor |
| `doc_vendor_ambermcpansatz_440506` | amber MCP-Ansatz | software_vendor |
| `doc_vendor_ai_d59357` | Generative AI & LLMs for Dummies | software_vendor |
| `doc_vendor_insurance_474aeb` | MSG Efficient Claims Management | software_vendor |
| `doc_industry_digitalesouveraenitaetbeltiosgdvwhitepaperausgabe22025_2025_913b5f` | Beltios/GDV Digitale Souveränität | industry_association |
| `doc_corporate_allianz_6ae771` | Allianz Tech-Konzern | corporate |
| `doc_corporate_digitalesschadenmanagement_846423` | R+V Digitales Schadenmanagement | corporate |

**Dokumentation** — vollständig überarbeitet und konsolidiert (Mai 2026)
- architecture.md
- status.md
- decisions.md
- technical_debt.md

---

### Offen / Nächste Schritte

**Priorität 1 — Trusted Advisor Bot**
- `bots/trusted_advisor_bot/` implementieren
- Primärer Use Case: Berater-Bot für Versicherungs-Consulting
- Knowledge Base mit 25 Dokumenten bereit

**Priorität 2 — Weitere technische Schulden**
- TD-005: Topic als Klassifikationsdimension
- TD-009: AUTHOR_ORIGIN_MAP Keyword-Qualität (Wort-Grenz-Matching)
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
| Embedding | sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 |
| Vektorindex | FAISS |
| LLM (Construction) | Claude claude-sonnet-4-6 (Anthropic API) |
| LLM (Query) | Claude claude-sonnet-4-6 (Anthropic API) |

---

## Bekannte Schwächen

- Kein Bot implementiert
- Kein Ingestion-Layer für Web-Quellen
- AUTHOR_ORIGIN_MAP verwendet Substring-Matching → potenzielle False Positives (TD-009)
