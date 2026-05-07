# Status – Strategic Knowledge Engine
Zuletzt aktualisiert: 2026-05-07

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
- Origin-Detection auf Titel + Dateiname beschränkt (kein Preview-Text)
- Classifier-Truncation entfernt: Preview-Größe über `PREVIEW_MAX_CHARS` gesteuert
- `supervisory_authority` → Prefix `doc_supervisory_*`
- OECD auf `research_institution` korrigiert
- `AUTHOR_ORIGIN_MAP` und `FILENAME_KEYWORDS` deutlich erweitert

**Media-Support** — abgeschlossen (2026-05-06)
- Neue Origin `media` in Taxonomy, Governance, Scoring, Doc-ID-Generator
- Neuer Document Type `press_article`
- `AUTHOR_ORIGIN_MAP` um SZ, FAZ, Handelsblatt, Spiegel, Manager Magazin u.a. erweitert

**TD-007: Governance-Korrekturen & Re-Onboarding** — abgeschlossen (2026-05-06)
- Ursachenanalyse: 7 Fehlklassifikationen auf 3 Governance-Lücken zurückgeführt
- `FILENAME_KEYWORDS["research_institution"]`: Formatbegriffe entfernt
  ("studie", "study", "report", "whitepaper" beschreiben Form, nicht Author)
- `DOCUMENT_TYPE_CORRECTIONS`: Regeln für supervisory_authority, consulting_firm,
  software_vendor, cloud_vendor vollständig ergänzt
- `LLM_DOMAIN_NORMALIZATION`: `transformation_strategy` ergänzt
- Cross-Field-Validation Fix: supervisory_authority-Regeln setzen `domain_layer=regulation`
- Vollständiges Re-Onboarding: 37 Dokumente, 0 Errors, 0 Review-Punkte
- `scripts/reclassify.py`: Operations-Tool für gezielte Einzelkorrekturen ohne Re-Onboarding
- Architekturprinzip dokumentiert: D-012 + "Ursache vor Symptom" (architecture.md)

**Internal Origin & conet-Support** — abgeschlossen (2026-05-07)
- Neue Origin `internal` für conet-eigene Dokumente in `AUTHOR_ORIGIN_MAP`
  (`conet`, `conet deutschland`, `conet deutschland gmbh`, `conet group`)
- `FILENAME_KEYWORDS["internal"]`: Keyword `conet` ergänzt
- Prioritätsreihenfolge in `FILENAME_KEYWORDS` korrigiert:
  `internal` vor `corporate` — verhindert False Match auf "allianz" in conet-Dateinamen
  `industry_association` vor `research_institution` — verhindert False Match auf "whitepaper"
- `portfolio_gtm` als neue Knowledge Domain (Keywords: offering, rfp, proposal, capabilities)
- Erstes internes Dokument ongeboardet:
  `doc_internal_conetrfpallianzbusinessproposal2026_2026_f74120`

---

## Knowledge Base (aktuell)

```
Dokumente : 26
Chunks    : 833
FAISS     : 833 entries
Konsistenz: ✔ OK
Stand     : 2026-05-07
```

Origin-Verteilung: consulting_firm 5 · supervisory_authority 5 · research_institution 4 ·
software_vendor 3 · cloud_vendor 2 · corporate 2 · internal 1 ·
industry_association 1 · legislator 1 · media 1 · aws 1

---

## Aktiver Use Case: Business Development / Insurance Offering (neu, 2026-05-07)

Ziel: Aufbau eines Insurance Offerings für conet auf Basis von:
- **Intern:** conet-Capabilities, Methoden, Positionierung (aus RfP-Dokumenten)
- **Extern:** Markttrends, Regulatorik, Studien, Wettbewerb (aus Knowledge Base)

Vorgehen:
1. Weitere RfP-Dokumente onboarden (Fragebogen, KI-Fragebogen, Präsentation)
2. Query-CLI nutzen für explorative Analyse (Gap/Fit intern ↔ extern)
3. Ggf. später: `business_development_bot` als strukturierte Anwendung auf der Engine

Entscheidung: Kein spezialisierter Bot in dieser Phase — Use Case ist explorativ,
nicht repetitiv. Direktzugang zur Engine via Query-CLI ist ausreichend.

---

## Offen

**Query-CLI** — nächster Schritt (Priorität 1)
- Ziel: direkter interaktiver Zugang zur Query Pipeline
- Kein Bot, keine Persona — Engine-Direktzugang mit Quellenangaben
- Umsetzung: `scripts/query_cli.py`
- Ausführung: `python -m scripts.query_cli`

**Weitere RfP-Dokumente onboarden**
- Fragebogen, KI-Fragebogen, Präsentation
- Namenskonvention: `conet_rfp_allianz_<typ>_2026.docx`

**Bot-Implementierung** — zurückgestellt
- `trusted_advisor_bot/`, `marketing_bot/`, `insurance_portfolio_bot/`
- Verzeichnisse vorhanden, Implementierung offen
- Priorisierung nach Abschluss der explorativen Phase

**Technical Debt** — 4 offene Punkte (siehe technical_debt.md)
- TD-004: Regressionstest auf Referenzdokumente begrenzen (niedrig)
- TD-005: Topic als Klassifikationsdimension einführen (mittel)
- TD-008: Ingestion-Layer für Web-Quellen (niedrig)
- TD-009: AUTHOR_ORIGIN_MAP Keyword-Qualität / Wort-Grenz-Matching (niedrig)

---

## Nächster Schritt

`scripts/query_cli.py` — interaktives Query-Interface direkt auf der Engine.
