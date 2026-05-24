# Status – Strategic Knowledge Engine
Zuletzt aktualisiert: 2026-05-25

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

**Knowledge Engine (Query-Seite)** — implementiert, validiert und produktiv.
- Intent Engine
- Role Engine
- Retrieval Engine (FAISS vector search, Document Aggregation)
- Scoring Engine (Governance-aware Ranking — neu: normalisiert und ausgewogen)
- Context Builder
- Prompt Governance
- QueryPipeline (End-to-End validiert mit echtem Claude)

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
- `DOCUMENT_TYPE_CORRECTIONS`: Regeln vollständig ergänzt
- `LLM_DOMAIN_NORMALIZATION`: `transformation_strategy` ergänzt
- Cross-Field-Validation Fix: supervisory_authority-Regeln setzen `domain_layer=regulation`
- Vollständiges Re-Onboarding: 37 Dokumente, 0 Errors, 0 Review-Punkte
- `scripts/reclassify.py`: Operations-Tool für Einzelkorrekturen ohne Re-Onboarding
- Architekturprinzip dokumentiert: D-012 + "Ursache vor Symptom" (architecture.md)

**Internal Origin & conet-Support** — abgeschlossen (2026-05-07)
- Neue Origin `internal` für conet-eigene Dokumente
- `portfolio_gtm` als neue Knowledge Domain
- Erstes internes Dokument ongeboardet: `doc_internal_conetrfpallianzbusinessproposal2026_2026_f74120`

**Query Interface & Retrieval-Validierung** — abgeschlossen (2026-05-07)

Query Interface `scripts/run_query.py` implementiert und validiert:
- Zwei Modi: `--retrieval-only` (kein LLM, kein API-Cost) und vollständige Pipeline
- Ausgabe: Intent, Role, RAW CHUNKS, RANKED DOCUMENTS (mit semantic/governance-Split),
  CONTEXT CHUNKS (Volltext), RESPONSE, DIAGNOSTICS inkl. Embedding-Modell

Scoring-Modell grundlegend überarbeitet (`config/scoring_config.py`, `scoring_engine.py`):
- **Vorher:** additives Modell — Governance-Offset dominierte semantische Relevanz strukturell
- **Nachher:** gewichtete Kombination `65% semantic + 35% governance`, beide Komponenten
  normalisiert auf 0–1. Governance korrigiert, aber kann semantische Relevanz nicht mehr
  vollständig überstimmen.
- Bot-Override vorbereitet: `config_override`-Parameter in ScoringEngine

Embedding-Modell konsolidiert:
- `paraphrase-multilingual-MiniLM-L12-v2` als einzige Quelle der Wahrheit in
  `config/construction_config.py`
- Alle Stellen (Scripts, Tests) lesen aus Config — kein hartkodierter Modellname mehr
- Vollständiges Re-Onboarding mit multilingual Modell durchgeführt

PerspectiveOrchestrator deaktiviert (Schritt 6 in QueryPipeline):
- Ersetzt durch score-basierte Top-k Selektion aus `CONTEXT_CONFIG`
- Begründung: Erzwungene Perspektiv-Quoten zogen inhaltlich schwache Chunks in den
  Context — bei aktueller KB-Größe überwiegen die Nachteile
- Reaktivierung sinnvoll wenn KB pro Perspektive ausreichend starke Dokumente hat

Score-Propagation implementiert (Schritt 5 in QueryPipeline):
- `doc.score` (governance-aware) wird auf jeden Chunk übertragen
- PerspectiveOrchestrator / Fallback nutzen finalen Score statt rohem similarity_score
- Fix: Governance-Arbeit der ScoringEngine blieb vorher im nächsten Schritt wirkungslos

`vector_top_k` auf 100 erhöht (war 60):
- DORA-Dokument (broad regulatory text, niedrige semantische Scores) erscheint nun
  konsistent im FAISS-Pool für DORA-spezifische Queries

End-to-End Validierung erfolgreich:
- Query: "Was fordert DORA hinsichtlich Cloud-Auslagerung bei Versicherungen?"
- Claude halluziniert nicht — gibt korrekte Einschränkung wenn Context unvollständig
- Nach Onboarding zweier DORA-spezifischer BaFin-Dokumente: Claude liefert substanzielle
  Antwort mit konkreten Artikelreferenzen (Art. 4, 28, 30 DORA)
- Quellen korrekt: BaFin DORA-Umsetzungshinweise Juni 2024, EIOPA, BaFin Cloud-Mitteilung

**TD-011: Min-Score-Threshold im ContextBuilder** — abgeschlossen (2026-05-07)
- Problem: Breit gefasste Research-Studien (z.B. score=0.252) lieferten irrelevante
  Chunks neben qualitativ starken Dokumenten (supervisory_authority score≥0.33)
- Lösung: `min_document_score: 0.30` in `CONTEXT_CONFIG` (engine_config.py)
- ContextBuilder filtert Chunks via `_get_chunk_score()` vor Selektion
- Score wird aus `chunk.document_metadata['score']` gelesen (Score-Propagation Schritt 5)
- Threshold config-driven — Tuning ohne Code-Change möglich

**`prompt_governance.py`: erweiterter System Prompt für trusted_advisor** — abgeschlossen (2026-05-25)
- `_system_prompt` auf alle 7 Knowledge Domains erweitert (inkl. Leadership & Management, Politik und Gesellschaft)
- Versicherungsmarkt-Hardcodierung entfernt — domainspezifischer Fokus gehört ins Bot-Prompting
- Dreier-Unterscheidung (Regulatory fact / Supervisory interpretation / Advisory judgment) auf beide Ebenen verteilt: Rollenidentität im System Prompt, imperatives Labeling in Instructions

**Taxonomie-Erweiterung: neue Knowledge Domains** — abgeschlossen (2026-05-24)
- Systemkontext erweitert: Versicherung, Cloud, Consulting, AI + Software-Architektur,
  Leadership & Management, Politik & Gesellschaft
- 3 neue `KNOWLEDGE_DOMAINS`: `software_architecture`, `leadership_management`, `politics_society`
- 9 neue `TOPICS`: software_design, system_architecture, engineering_practices, leadership,
  team_management, organizational_development, politics, public_policy, society_technology
- `DOMAIN_KEYWORDS`: neue Keyword-Sets für alle 3 Domains
- `DOMAIN_PRIORITY`: neue Domains am Ende der Prioritätsliste ergänzt
- `LLM_DOMAIN_NORMALIZATION`: 7 neue Mappings für LLM-Abweichungen
- Geänderte Dateien: `config/taxonomy.py`, `config/governance_config.py`
- Kein Re-Onboarding des Bestands erforderlich — neue Domains greifen nur bei neuen Dokumenten

---

## Knowledge Base (aktuell)

```
Dokumente : 81
Chunks    : 1777
FAISS     : 1777 entries
Konsistenz: ✔ OK
Stand     : 2026-05-07
Modell    : paraphrase-multilingual-MiniLM-L12-v2
```

Origin-Verteilung:
```
software_vendor        16
consulting_firm        16
research_institution   11
media                  11
supervisory_authority   8
cloud_vendor            7
corporate               7
industry_association    3
internal                1
legislator              1
```

---

## Aktiver Use Case: Business Development / Insurance Offering

Ziel: Aufbau eines Insurance Offerings für conet auf Basis von:
- **Intern:** conet-Capabilities, Methoden, Positionierung (aus RfP-Dokumenten)
- **Extern:** Markttrends, Regulatorik, Studien, Wettbewerb (aus Knowledge Base)

Vorgehen:
1. ✔ Query-Interface implementiert und validiert
2. Query-CLI für explorative Analyse nutzen
3. Ggf. später: `business_development_bot` als strukturierte Anwendung auf der Engine

Entscheidung: Kein spezialisierter Bot in dieser Phase — Use Case ist explorativ,
nicht repetitiv. Direktzugang zur Engine via `scripts/run_query.py` ist ausreichend.

---

## Offen

**Query-Validierung fortsetzen**
- Weitere Queries mit verschiedenen Themen testen (Cloud-Strategie, KI, Regulatorik)
- Qualität und Korrektheit der Antworten systematisch beurteilen

**Weitere Dokumente onboarden**
- Weitere conet RfP-Dokumente (Fragebogen, KI-Fragebogen, Präsentation)
- EIOPA RTS/ITS zu DORA für Versicherungen
- VAIT (Versicherungsaufsichtliche Anforderungen an die IT)
- Erste Dokumente für neue Domains: software_architecture, leadership_management, politics_society

**Bot-Implementierung** — zurückgestellt
- `trusted_advisor_bot/`, `marketing_bot/`, `insurance_portfolio_bot/`
- Verzeichnisse vorhanden, Implementierung offen
- Priorisierung nach Abschluss der explorativen Phase

**Technical Debt** — 6 offene Punkte (siehe technical_debt.md)
- TD-004: Regressionstest auf Referenzdokumente begrenzen (niedrig)
- TD-005: Topic als Klassifikationsdimension einführen (mittel)
- TD-008: Ingestion-Layer für Web-Quellen (niedrig)
- TD-009: AUTHOR_ORIGIN_MAP Keyword-Qualität (niedrig)
- TD-012: Chunk-Strategie überprüfen (niedrig)
- TD-013: Unterstrich-Normalisierung in Origin-Erkennung (mittel)

---
