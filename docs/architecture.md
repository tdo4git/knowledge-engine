# Architecture – Strategic Knowledge Engine
Version: 3.3

---

## Zielbild

Die Strategic Knowledge Engine ist ein mehrschichtiges, KI-gestütztes
Wissensmanagementsystem für den beruflichen Kontext in den Bereichen
Versicherung, Cloud, Consulting, AI, Software-Architektur, Leadership & Management
sowie Politik und Gesellschaft.
Strikte Trennung von Wissenserstellung und Wissensnutzung.
Explainability und Governance sind erstklassige Architekturprinzipien.

---

## Systemstruktur

```
Document Sources
→ Knowledge Construction
→ Knowledge Base
→ Knowledge Engine
→ Bots
```

---

## 1. Document Sources

```
knowledge_sources/
  intake/         ← Dropzone für neue Dokumente
  archive/        ← kuratierte Originale
  raw_sensitive/  ← interne / vertrauliche Dokumente
```

Unterstützte Formate: PDF, DOCX, TXT

---

## 2. Knowledge Construction Pipeline

```
Dokument
→ Preview Extraction       (~6000 Zeichen für Klassifikation)
→ Document Classification  (LLM-basiert, YAML contract-driven)
→ Governance Rules         (deterministisch, zentralisiert)
→ Validation               (Enum + Cross-Field)
→ Registry Entry
→ Text Extraction
→ Token-based Chunking
→ Embedding Generation     (paraphrase-multilingual-MiniLM-L12-v2)
→ FAISS Index Update
→ Consistency Check
→ Audit Log
```

Start: `python -m scripts.<script_name>` aus `knowledge-engine/`

---

## 3. Knowledge Base

Read-only zur Laufzeit. Ausschließlich durch Construction Pipeline erzeugt.

```
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
```

Beziehung: `document_registry` → `doc_id` → `chunks` → index alignment → `embeddings`

---

## 4. Knowledge Engine (Query Pipeline)

```
Query
→ Intent Engine
→ Role Engine
→ Retrieval Engine       (FAISS vector search → Chunk Candidates → Document Aggregation)
→ Scoring Engine         (Governance-aware Ranking)
→ Context Builder        (max_documents=5, max_chunks_per_document=2, min_score=0.30)
→ [Perspective Orchestrator deaktiviert — score-basierte Top-k Selektion]
→ Prompt Governance
→ LLM
→ Answer
```

Zentrales Datenobjekt: `QueryContext` — trägt gesamten Zustand durch die Pipeline.
Einstiegspunkt: `QueryPipeline.run(query)` — einzige erlaubte Orchestrierungsschicht.

---

## 5. Bots

Anwendungen auf der Engine. Teilen dieselbe Knowledge Base und Engine.
Unterscheiden sich durch Prompting, Tonalität und Use Case.

```
bots/
  trusted_advisor_bot/     ← primärer Use Case
  marketing_bot/
  insurance_portfolio_bot/
```

Status: Verzeichnisse vorhanden, Implementierung offen.

---

## Repository-Struktur

```
knowledge-engine/
  knowledge_core/
    intent/
    roles/
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
  bots/
  knowledge_sources/
  config/
  scripts/
  tests/
  docs/
```

---

## Architekturprinzipien (non-negotiable)

- **Separation of Concerns**: Knowledge Construction ↔ Knowledge Retrieval strikt getrennt
- **Governance zentralisiert**: alle Governance-Logik läuft durch `apply_governance()` — keine verteilte Logik
- **LLM erzeugt keine Fakten**: ausschließlich auf Basis selektierter Dokumente
- **Explainability Pflicht**: jede Antwort rückverfolgbar auf `doc_id → chunk_id → registry → scoring`
- **Taxonomie als Single Source of Truth**: `config/taxonomy.py` — nur definierte Werte erlaubt
- **Pfadlogik**: `BASE_PATH = Path(__file__).resolve().parent.parent`
- **Script-Ausführung**: immer als Module `python -m scripts.<name>`
- **Keine Architektur-Brüche**, keine Workarounds
- **Ursache vor Symptom**: Fehlklassifikationen werden durch Governance-Korrekturen behoben,
  nicht durch manuelle Nachbearbeitung. Das Reklassifizierungs-Skript ist Bestandsbereinigung,
  kein Ersatz für korrekte Governance-Regeln.

---

## Taxonomie (Schlüsseldimensionen)

| Dimension | Zweck |
|---|---|
| `document_type` | Art des Dokuments (regulatory_text, blog_article, ...) |
| `origin` | Herkunft (legislator, supervisory_authority, consulting_firm, ...) |
| `domain_layer` | Abstraktionsebene (regulation, business, technology, strategy, market) |
| `knowledge_domain` | Wissenskontext (insurance_domain, cloud_technology, ...) |
| `jurisdiction` | Rechtsraum (EU, Germany, Global, ...) |
| `bias_level` | Eingeschätzter Bias (very_low → elevated) |
| `confidence` | Klassifikationssicherheit (0.0 – 1.0) |

Vollständige Definition: `config/taxonomy.py`

---

## Scoring-Modell

Governance-aware Ranking basiert auf:
- Origin Weight (regulatorische Quellen > advisory > marketing)
- Confidence Weight
- Document Type Weight
- Semantische Ähnlichkeit (FAISS cosine similarity)

Konfiguration: `config/scoring_config.py`

---

## LLM-Interaktionsmodell

Contract-driven — keine hardcodierten Prompts:

```
YAML Contract → Prompt Builder → LLMClient → LLM
```

Produktiv: Claude (`claude-sonnet-4-6`) via Anthropic API (seit 2026-05-01)
DummyLLM ausschließlich in Tests als Isolations-Hilfsmittel.
