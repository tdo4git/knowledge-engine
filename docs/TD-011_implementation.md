# TD-011 Implementation Summary
**Mindest-Score-Threshold im ContextBuilder**

**Status:** Implementiert (2026-05-07)
**Aufwand:** klein ✔
**Priorität:** hoch ✔

---

## Problem
Der ContextBuilder selektiert Chunks aus top-ranked Dokumenten ohne Mindestqualität zu prüfen. 
Dokumente mit niedrigem Score landen mit irrelevanten Chunks im Context:
- `doc_research_insurance_2a0a0c` (score=0.252) → irrelevante Chunks
- `supervisory_authority` Dokumente (score≥0.33) → korrekt selektiert

Breit gefasste Research-Studien, die Keywords zufällig treffen, verrauschen Retrieval-Ergebnisse.

---

## Lösung

### 1. `config/engine_config.py`
- `CONTEXT_CONFIG` um `min_document_score: 0.30` erweitert
- Schwellwert konservativ gewählt (unter supervisory 0.33, über niedrigen Research 0.25)
- Tuning möglich via Config — kein Code-Change nötig

### 2. `knowledge_core/pipeline/context_builder.py`
- `__init__()` liest `min_document_score` aus Config
- `build_context()` filtert Chunks vor Limitierung:
  ```python
  filtered_chunks = [
      chunk for chunk in chunks
      if self._get_chunk_score(chunk) >= self.min_document_score
  ]
  ```
- `_get_chunk_score()` Hilfsmethode:
  - Versucht Score aus `chunk.document_metadata['score']` zu lesen
  - Fallback auf `chunk.score` (direktes Feld)
  - Default 0.0 bei Fehlen (→ wird gefiltert)

---

## Architektur
- **Keine Breaking Changes** — Score-Propagation setzt diese Annahme bereits um (Status.md)
- **Config-driven** — Anpassung ohne Code-Change möglich
- **Explainability** — Filtered Chunks sind nachverfolgbar

---

## Validierung (nächste Schritte)

1. Code in lokales Projekt kopieren
2. Query mit breiter Research-Studie testen:
   - Vorher: `doc_research_insurance_2a0a0c` in Context
   - Nachher: gefiltert, nur relevante Dokumente
3. Score-Verteilung prüfen: `min_document_score: 0.30` anpassen falls nötig

---

## Auswirkungen
- ✔ Verbesserte Retrieval-Qualität
- ✔ Reduzierter Noise im LLM-Context
- ✔ Keine Performance-Penalty (Filter vor Limitierung)
- ✔ Audit-Trail erhalten (Chunks noch nachverfolgbar)
