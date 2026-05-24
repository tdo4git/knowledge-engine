# Strategic Knowledge Engine — Claude Code Context

## Projekt

KI-basiertes Wissensmanagementsystem für den beruflichen Kontext in den Bereichen
Versicherung, Cloud, Consulting, AI, Software-Architektur, Leadership & Management
sowie Politik und Gesellschaft.

Mehrschichtiges RAG-System mit strikter Trennung von Wissenserstellung und Wissensnutzung.
Explainability und Governance sind erstklassige Architekturprinzipien.

**Stack:** Python, VS Code, lokal auf MacBook  
**LLM:** Claude (`claude-sonnet-4-6`) via Anthropic API  
**Stand:** 2026-05-24 — Construction + Query Pipeline produktiv. Bots offen.

---

## Architekturprinzipien (non-negotiable)

1. **Separation of Concerns** — Knowledge Construction ↔ Knowledge Retrieval strikt getrennt. Knowledge Base ist zur Laufzeit read-only.
2. **Governance zentralisiert** — alle Governance-Logik läuft ausschließlich durch `apply_governance()`. Keine Governance-Logik außerhalb der zentralen Pipeline.
3. **LLM erzeugt keine Fakten** — Antworten ausschließlich auf Basis selektierter Dokumente aus der Knowledge Base.
4. **Explainability Pflicht** — jede Antwort rückverfolgbar auf `doc_id → chunk_id → registry → scoring`.
5. **Taxonomie als Single Source of Truth** — `config/taxonomy.py` ist die einzige Quelle für erlaubte Klassifikationswerte. Keine freien Klassifikationen.
6. **Ursache vor Symptom** — Fehlklassifikationen durch Governance-Korrekturen beheben, nicht durch manuelle Nachbearbeitung. Reklassifizierungs-Skript ist Bestandsbereinigung, kein Ersatz.
7. **Keine Architektur-Brüche** — keine Workarounds, keine Abkürzungen.
8. **Bots sind Schicht über der Engine** — teilen Knowledge Base + Engine, unterscheiden sich durch Prompting und Use Case. Keine Bot-Logik in der Engine.

---

## Konventionen

**Pfadlogik:**
```python
BASE_PATH = Path(__file__).resolve().parent.parent
```

**Script-Ausführung** — immer als Module aus `knowledge-engine/`:
```bash
python -m scripts.<script_name>
```

**LLM-Modell:** `claude-sonnet-4-6`  
**API Key:** via `.env` → `ANTHROPIC_API_KEY`

---

## Systemstruktur

```
Document Sources
→ Knowledge Construction   (knowledge_construction/)
→ Knowledge Base           (knowledge_base/)  ← read-only zur Laufzeit
→ Knowledge Engine         (knowledge_core/)
→ Bots                     (bots/)
```

### Knowledge Construction Pipeline
```
Dokument
→ Preview Extraction (~6000 Zeichen)
→ Document Classification (LLM, YAML contract-driven)
→ Governance Rules (deterministisch, zentralisiert)
→ Validation (Enum + Cross-Field)
→ Registry Entry → Chunking → Embedding → FAISS Index Update → Audit Log
```

### Query Pipeline (QueryPipeline.run(query) — einziger Einstiegspunkt)
```
Query
→ Intent Engine
→ Role Engine
→ Retrieval Engine (FAISS, vector_top_k=100)
→ Scoring Engine (65% semantic + 35% governance, normalisiert)
→ Score-Propagation (doc.score → Chunks)
→ [PerspectiveOrchestrator deaktiviert — score-basierte Top-k Selektion]
→ Context Builder (max_documents=5, max_chunks_per_doc=2, min_score=0.30)
→ Prompt Governance
→ LLM
→ Answer
```

**Zentrales Datenobjekt:** `QueryContext` — trägt gesamten Zustand durch die Pipeline.

### Scoring-Modell (aktuell)
- **65% semantic** (FAISS cosine similarity) + **35% governance** (Origin/Confidence/DocType)
- Beide Komponenten normalisiert auf 0–1
- Governance korrigiert, kann semantische Relevanz aber nicht mehr vollständig überstimmen
- Bot-Override vorbereitet: `config_override`-Parameter in `ScoringEngine`
- Konfiguration: `config/scoring_config.py`

### LLM-Interaktionsmodell
```
YAML Contract → Prompt Builder → LLMClient → LLM
```
Keine hardcodierten Prompts. Contracts in `knowledge_construction/llm/contracts/`.

---

## Zwei LLM-Clients

| Client | Pfad | Zweck | Temp | Output |
|---|---|---|---|---|
| Construction | `knowledge_construction/llm/llm_client.py` | Klassifikation | niedrig | JSON |
| Engine | `knowledge_core/llm/llm_client.py` | Query-Antworten | 0.3 | Text |

---

## Repository-Struktur

```
knowledge-engine/
  knowledge_core/
    intent/ | roles/ | retrieval/ | scoring/ | perspective/ | prompt/ | pipeline/
  knowledge_construction/
    metadata/ | validation/ | governance/ | registry/ | chunking/ | embedding/
    document_processing/ | llm/ | onboarding_pipeline.py
  knowledge_base/
    registry/document_registry.json
    chunks/chunks.json
    vector_index/  (embeddings.pt, chunk_ids.json, index.faiss)
    audit/         (onboarding_audit_log.jsonl, review_report.txt)
  bots/
    trusted_advisor_bot/     ← primär, offen
    marketing_bot/           ← offen
    insurance_portfolio_bot/ ← offen
  knowledge_sources/
    intake/    ← Dropzone für neue Dokumente
    archive/   ← kuratierte Originale (nach Onboarding automatisch verschoben)
    raw_sensitive/
  config/
    taxonomy.py          ← Single Source of Truth für alle Klassifikationswerte
    scoring_config.py
    construction_config.py
    engine_config.py
  scripts/
    run_query.py         ← Query Interface (--retrieval-only | vollständig)
    reclassify.py        ← Einzelkorrekturen ohne Re-Onboarding
    generate_snapshot.py
  tests/
  docs/
```

---

## Taxonomie (Schlüsseldimensionen)

| Dimension | Zweck |
|---|---|
| `document_type` | regulatory_text, blog_article, press_article, consulting_framework, ... |
| `origin` | legislator, supervisory_authority, consulting_firm, media, corporate, internal, ... |
| `domain_layer` | regulation, business, technology, strategy, market |
| `knowledge_domain` | insurance_domain, cloud_technology, ai_genai_agentic, portfolio_gtm, software_architecture, leadership_management, politics_society, ... |
| `jurisdiction` | EU, Germany, Global, ... |
| `bias_level` | very_low → elevated |
| `confidence` | 0.0 – 1.0 |

Vollständige Definition: `config/taxonomy.py`

---

## Knowledge Base (Stand 2026-05-07)

```
Dokumente : 81  |  Chunks : 1777  |  FAISS : 1777 entries  |  Konsistenz: ✔ OK
Embedding : paraphrase-multilingual-MiniLM-L12-v2
```

Origin-Verteilung:
```
software_vendor (16) | consulting_firm (16) | research_institution (11) | media (11)
supervisory_authority (8) | cloud_vendor (7) | corporate (7)
industry_association (3) | internal (1) | legislator (1)
```

---

## Offener Technical Debt

| ID | Bereich | Beschreibung | Priorität |
|---|---|---|---|
| TD-004 | Tests | Regressionstest auf 3–5 Referenzdokumente begrenzen | niedrig |
| TD-005 | Klassifikation | `topic` als eigene Dimension in Registry + Scoring einführen | mittel |
| TD-008 | Knowledge Sources | Ingestion-Layer für Web-Quellen (LinkedIn, Blog, Podcast) | niedrig |
| TD-009 | Governance | Wort-Grenz-Matching in `AUTHOR_ORIGIN_MAP` statt Substring | niedrig |
| TD-012 | Chunking | Chunk-Strategie evaluieren (400 Token / semantisch) | niedrig |
| TD-013 | Governance | Unterstrich-Normalisierung in Origin-Erkennung (`_apply_origin`) | mittel |

---

## Was als nächstes kommt

**Kurzfristig:**
- Query-Validierung fortsetzen (Cloud-Strategie, KI, Regulatorik)
- Weitere Dokumente onboarden: conet RfP-Fragebogen, EIOPA RTS/ITS, VAIT
- Erste Dokumente für neue Domains: `software_architecture`, `leadership_management`, `politics_society`

**Zurückgestellt:**
- Bot-Implementierung (`trusted_advisor_bot`, `marketing_bot`, `insurance_portfolio_bot`)
- Priorisierung nach Abschluss der explorativen Phase

**Aktiver Use Case:** Business Development / Insurance Offering (conet)  
→ Direktzugang via `scripts/run_query.py` — kein spezialisierter Bot in dieser Phase

---

## Working Style

- Kurz und präzise — keine langen Herleitungen
- Vollständige, direkt verwendbare Dateien
- Kritisch bei Architektur- und Designentscheidungen
- Keine unnötigen Bestätigungen oder Wiederholungen
- Priorität: Korrektheit → Umsetzbarkeit → Klarheit → Kürze
