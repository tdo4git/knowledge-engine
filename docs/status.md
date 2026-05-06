# Status – Strategic Knowledge Engine
Zuletzt aktualisiert: 2026-05-06

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
- TD-010 implizit gelöst: `generate_doc_id()` läuft nach Governance, verwendet finale Origin

**Governance & Klassifikation** — stabilisiert (2026-05-03)
- Origin-Detection auf Titel + Dateiname beschränkt (kein Preview-Text) → verhindert False Positives durch regulatorischen Inhalt
- Classifier-Truncation entfernt: Preview-Größe ausschließlich über `PREVIEW_MAX_CHARS` in `construction_config.py` gesteuert
- `supervisory_authority` → Prefix `doc_supervisory_*` statt `doc_bafin_*`
- `corporate` in `_normalize_origin` ergänzt → `doc_corporate_*` korrekt
- OECD von `supervisory_authority` auf `research_institution` korrigiert
- `AUTHOR_ORIGIN_MAP` und `FILENAME_KEYWORDS` deutlich erweitert (Capgemini, BearingPoint, Lünendonk, Trendzowl, heise, amber, Beltios, R+V, adesso u.a.)

**Media-Support** — abgeschlossen (2026-05-06)
- Neue Origin `media` in Taxonomy, Governance, Scoring, Doc-ID-Generator
- Neuer Document Type `press_article` in Taxonomy und Scoring
- `AUTHOR_ORIGIN_MAP` um SZ, FAZ, Handelsblatt, Spiegel, Manager Magazin u.a. erweitert
- `FILENAME_KEYWORDS["media"]` ergänzt — Dateiname-Präfix "SZ" triggert direkt `filename_rule`
- DOCUMENT_TYPE_CORRECTION: `media + blog_article → press_article`
- ORIGIN DETECTION GUIDANCE im Classifier-Prompt um MEDIA-Block ergänzt
- Scoring: `media: -0.1` (origin), `press_article: -0.05` (document_type)
- 11 SZ-Artikel erfolgreich ongeboardet

**Tooling** — abgeschlossen (2026-05-06)
- `scripts/generate_snapshot.py` neu: erzeugt kompakten System-Snapshot (Registry, Chunks, FAISS, Intake, Audit Log) für Claude-Kontext

**Knowledge Base** — 37 Dokumente, 868 Chunks, 0 Review-Punkte (2026-05-06)

| Doc-ID | Dokument | Origin | Type |
|---|---|---|---|
| `doc_supervisory_cloud_2024_53f735` | BaFin Cloud Outsourcing 2024 | supervisory_authority | supervisory_guidance |
| `doc_supervisory_insurance_83c73b` | EIOPA Digitalisation Report | supervisory_authority | research_report ⚠ |
| `doc_supervisory_cloud_a51b3a` | EIOPA Cloud & AI Future | supervisory_authority | expert_opinion |
| `doc_supervisory_stellungnahmemenschundmaschinekurzfassung_6ba9b6` | Stellungnahme Mensch & Maschine | supervisory_authority | expert_opinion |
| `doc_supervisory_20250903versicherungsmarktbericht2024_2025_10cbfd` | BaFin Versicherungsmarktbericht 2024 | supervisory_authority | research_report ⚠ |
| `doc_eu_dora_2022_0eb896` | DORA Verordnung EU 2022 | legislator | regulatory_text |
| `doc_consulting_dora_2024_d54141` | Exxeta DORA Practical Guide | consulting_firm | blog_article ⚠ |
| `doc_consulting_playbookbearingpointversicherung2030_2030_717627` | BearingPoint Playbook Versicherung 2030 | consulting_firm | consulting_framework |
| `doc_consulting_insurance_2024_19f71c` | Capgemini P&C Top Trends 2024 | consulting_firm | research_report ⚠ |
| `doc_consulting_insurance_2030_131197` | Claims 2030 Talent Strategy | consulting_firm | research_report ⚠ |
| `doc_consulting_sind_2026_0b05a4` | IT-Trends 2026 | consulting_firm | blog_article |
| `doc_research_insurance_2025_abeb26` | Global Insurance Report 2025 | research_institution | research_report |
| `doc_research_insurance_2025_1ebdd0` | OECD Global Insurance Market Trends 2025 | research_institution | research_report |
| `doc_research_insurance_2a0a0c` | Lünendonk Digital Outlook Insurance | research_institution | research_report |
| `doc_research_elingassekuranz20302_2030_3862f3` | Eling Assekuranz 2030 | research_institution | research_report |
| `doc_research_insurance_2025_588dcd` | Trendzowl Insurance Trends 2025 | research_institution | research_report |
| `doc_research_digitalesouveraenitaetbeltiosgdvwhitepaperausgabe22025_2025_913b5f` | Beltios/GDV Digitale Souveränität | research_institution ⚠ | research_report |
| `doc_aws_sovereignty_1c18e9` | AWS Digital Sovereignty Framework | cloud_vendor | vendor_marketing |
| `doc_aws_cloud_95e9f7` | AWS Insurance on the Cloud | cloud_vendor | vendor_marketing |
| `doc_vendor_heiseacademymycompany_6d0ccf` | HeiseAcademy MyCompany GPT | software_vendor | research_report ⚠ |
| `doc_vendor_ambermcpansatz_440506` | amber MCP-Ansatz | software_vendor | vendor_marketing |
| `doc_vendor_ai_d59357` | Generative AI & LLMs for Dummies | software_vendor | vendor_marketing |
| `doc_vendor_insurance_474aeb` | MSG Efficient Claims Management | software_vendor | blog_article |
| `doc_internal_conetrfpallianzbusinessproposal2026_2026_f74120` | Conet RFP Allianz Business Proposal 2026 | internal | consulting_framework |
| `doc_corporate_allianz_6ae771` | Allianz Tech-Konzern | corporate | blog_article |
| `doc_corporate_digitalesschadenmanagement_846423` | R+V Digitales Schadenmanagement | corporate | blog_article |
| `doc_media_digitale_dec231` | SZ — Digitale Souveränität: Zwei Drittel bevorzugen EU-Firmen | media | press_article |
| `doc_media_digitale_7fb28c` | SZ — Europas Tech-Abhängigkeit: so riskant | media | press_article |
| `doc_media_eusouveranitat_27bf6a` | SZ — EU-Souveränität und USA | media | press_article |
| `doc_media_versicherer_fdc5e6` | SZ — Versicherer: keine Rolle mehr | media | press_article |
| `doc_media_europas_38857c` | SZ — Europas Souveränität: digital erwachsen werden | media | press_article |
| `doc_media_microsoft_ccf347` | SZ — Microsoft und KI: Frage der Souveränität | media | press_article |
| `doc_media_kunstliche_b4ae99` | SZ — KI: Zusammen sind sie weniger allein | media | press_article |
| `doc_media_ai_2934fe` | SZ — IT-Sicherheit: AI-pokalypse | media | press_article |
| `doc_media_kunstliche_8d77be` | SZ — KI: Wo die Grenzen liegen sollten | media | press_article |
| `doc_media_kunstliche_859301` | SZ — KI-Agenten: Der Hype ist gefährlich | media | press_article |
| `doc_media_kunstliche_8f5fba` | SZ — KI: Blase? Welche Blase? | media | press_article |

⚠ = Fehlklassifikation, Kandidat für TD-007 (Reklassifizierung)

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
- Knowledge Base mit 37 Dokumenten bereit

**Priorität 2 — Reklassifizierung (TD-007)**
- 6 Dokumente mit fehlerhaftem Document Type (⚠ in Tabelle oben)
- 1 Dokument mit falscher Origin: Beltios/GDV → `industry_association` statt `research_institution`

**Priorität 3 — Weitere technische Schulden**
- TD-005: Topic als Klassifikationsdimension (4 SZ-KI-Artikel haben generischen Prefix `kunstliche`)
- TD-009: AUTHOR_ORIGIN_MAP Keyword-Qualität (Wort-Grenz-Matching) — relevant auch für Media-Einträge
- TD-004: Regressionstest auf Referenzdokumente begrenzen
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
- 7 Dokumente mit Fehlklassifikation im Document Type oder Origin → TD-007
