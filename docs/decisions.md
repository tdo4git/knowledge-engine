# Decisions – Strategic Knowledge Engine
Architektur- und Designentscheidungen mit Begründung

---

## Zweck

Dieses Dokument erklärt *warum* das System so gebaut wurde wie es ist.
Es verhindert, dass Entscheidungen unbewusst rückgängig gemacht werden
und macht das System erklärbar — für Dritte und für zukünftige Chats.

---

## D-001: Strikte Trennung Construction ↔ Retrieval

**Entscheidung:** Knowledge Construction und Knowledge Retrieval sind vollständig getrennte
Subsysteme. Die Knowledge Base ist zur Laufzeit read-only.

**Begründung:**
- Wissen wird einmal erstellt, viele Male abgefragt — unterschiedliche Anforderungen
- Qualitätssicherung (Governance, Validation) gehört in die Construction, nicht in die Query
- Immutable Knowledge Base ermöglicht reproduzierbare, erklärbare Ergebnisse
- Cloud-Migration wird vereinfacht: beide Subsysteme können unabhängig skaliert werden

---

## D-002: Governance ist zentralisiert

**Entscheidung:** Alle Governance-Logik läuft ausschließlich durch `apply_governance()`.
Keine Governance-Logik außerhalb der zentralen Pipeline.

**Begründung:**
- Verteilte Governance-Logik führt zu inkonsistenten Ergebnissen
- Zentralisierung macht das System auditierbar und testbar
- Änderungen an Governance-Regeln wirken sich konsistent auf alle Dokumente aus

---

## D-003: Taxonomie als Single Source of Truth

**Entscheidung:** Alle erlaubten Klassifikationswerte sind ausschließlich in `config/taxonomy.py`
definiert. Freie Klassifikationen sind nicht erlaubt.

**Begründung:**
- Konsistenz der Knowledge Base über alle Dokumente
- Retrieval und Scoring basieren auf stabilen, definierten Werten
- Taxonomie-Änderungen sind kontrolliert und nachvollziehbar
- LLM-Klassifikation wird durch Taxonomie eingeschränkt → keine Halluzination bei Metadaten

---

## D-004: LLM erzeugt keine Fakten

**Entscheidung:** Das LLM formuliert ausschließlich auf Basis der vom Context Builder
bereitgestellten, selektierten Dokumente. Es darf keine eigenen Fakten einbringen.

**Begründung:**
- Vertrauenswürdigkeit im Consulting-Kontext: Antworten müssen auf nachweisbaren Quellen basieren
- Regulatorische Dokumente (DORA, VAIT etc.) erfordern präzise, quellenbasierte Aussagen
- Explainability: jede Aussage muss auf doc_id → chunk_id rückverfolgbar sein

---

## D-005: Document-centric Retrieval

**Entscheidung:** Das Retrieval aggregiert Chunk-Kandidaten zu Dokument-Kandidaten.
Ranking und Kontext-Selektion arbeiten auf Dokumentebene, nicht auf Chunk-Ebene.

**Begründung:**
- Einzelne Chunks sind oft zu fragmentiert für sinnvolle Antworten
- Dokument-Kontext (Origin, Confidence, Bias) ist für Governance-Scoring notwendig
- Verhindert, dass viele Chunks desselben Dokuments den Kontext dominieren

---

## D-006: Contract-driven Prompt-Generierung

**Entscheidung:** Prompts werden nicht hardcodiert, sondern aus YAML-Contracts generiert.
Kein Prompt-Logik im LLMClient.

```
YAML Contract → Prompt Builder → LLMClient
```

**Begründung:**
- Prompts sind konfigurierbar ohne Code-Änderungen
- Verschiedene Bots können verschiedene Contracts verwenden
- Testbarkeit: Prompt Builder kann unabhängig vom LLM getestet werden
- Zukünftige Optimierung von Prompts ohne Architektur-Eingriff

---

## D-007: FAISS als Vektorindex

**Entscheidung:** FAISS (Facebook AI Similarity Search) als lokaler Vektorindex.

**Begründung:**
- Läuft vollständig lokal auf MacBook — keine Cloud-Abhängigkeit
- Performant auch für größere Dokumentmengen
- Einfache Migration zu Cloud-Lösungen (Pinecone, Weaviate) später möglich
- Keine laufenden Kosten in der Entwicklungsphase

---

## D-008: sentence-transformers/all-MiniLM-L6-v2 als Embedding-Modell

**Entscheidung:** Leichtgewichtiges Embedding-Modell für lokalen Betrieb.

**Begründung:**
- Läuft effizient auf MacBook ohne GPU
- Ausreichende Qualität für semantische Suche im Fachkontext
- Kann später durch ein stärkeres Modell ersetzt werden (nur Embeddings neu generieren)

**Offene Frage:** Für deutschsprachige Dokumente könnte ein mehrsprachiges Modell
(z.B. `paraphrase-multilingual-MiniLM-L12-v2`) bessere Ergebnisse liefern. Noch nicht evaluiert.

---

## D-009: Ziel-LLM ist Claude (Anthropic API)

**Entscheidung:** Das produktive LLM wird Claude (claude-sonnet-4-6) via Anthropic API.
Aktuell noch DummyLLM als Platzhalter.

**Begründung:**
- Lernziel: Anthropic-Tools kennenlernen und erklären können
- Claude eignet sich gut für document-grounded reasoning
- Anthropic API ermöglicht später auch Nutzung für Knowledge Construction (Klassifikation)
- Kostenkontrolle: Prompt Caching und Batch API reduzieren Kosten

**Noch offen:** API Key beschaffen, LLMClient implementieren.

---

## D-010: QueryPipeline als einziger Einstiegspunkt

**Entscheidung:** `QueryPipeline.run(query)` ist die einzige erlaubte Orchestrierungsschicht
für produktive Nutzung. Direkter Zugriff auf einzelne Engine-Komponenten nur für Tests.

**Begründung:**
- Konsistente Verarbeitung aller Queries (Intent → Role → Retrieval → ... → LLM)
- QueryContext-Objekt trägt vollständigen Zustand → Explainability und Debugging
- Anti-Pattern verhindert: kein LLM ohne Context Builder, kein Scoring außerhalb der Pipeline

---

## D-011: Bots als separate Schicht über der Engine

**Entscheidung:** Bots sind Anwendungen *auf* der Engine, nicht Teil der Engine.
Sie teilen dieselbe Knowledge Base und Engine, unterscheiden sich durch Prompting und Use Case.

**Begründung:**
- Engine bleibt generisch und wiederverwendbar
- Bot-spezifische Logik (Tonalität, Rollenverhalten) gehört nicht in die Engine
- Mehrere Bots können parallel betrieben werden ohne Engine-Änderungen
