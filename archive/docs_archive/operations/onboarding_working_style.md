## Kontext: Knowledge Engine – Onboarding & Validation Setup

Ich arbeite an einer Strategic Knowledge Engine mit einem strukturierten Onboarding- und Validierungsprozess für Dokumente.

### Ziel
Sicherstellen, dass:
- Dokumente korrekt klassifiziert werden (LLM + Governance)
- Metadaten konsistent und valide sind
- Änderungen am Onboarding keine Regressionen verursachen

---

## 🧩 Onboarding Pipeline (vereinfacht)

1. Dokument liegt im `intake/`
2. Onboarding Pipeline läuft:
   - Text Extraction
   - Chunking
   - Embeddings
   - Classification (LLM)
   - Governance (regelbasiert)
   - doc_id Generierung
3. Ergebnis wird in Registry gespeichert

---

## 🧠 Architekturprinzipien

- LLM liefert Vorschlag (unsicher)
- Governance korrigiert deterministisch
- Config enthält alle Regeln (keine Hardcodes)
- Classifier enthält KEINE Business-Logik

---

## 🆔 doc_id Design (wichtig!)

doc_id ist:
- generiert
- stabil
- ohne Metadaten

Beispiel:
doc_dora_regulation_2022

doc_id enthält NICHT:
- origin
- jurisdiction
- Klassifikationsattribute

---

## 🧪 Test-Setup: run_onboarding_validation (V4++)

### Ablauf

1. Reset Knowledge Base
   - archive → intake kopieren
   - knowledge_base leeren

2. Onboarding ausführen

3. Registry laden

4. Expectations laden

5. Matching:
   - doc_id_pattern
   - title_contains
   - optional source_file

6. Validierung:
   - doc_id_rules (z. B. forbidden substrings)
   - strict (muss exakt matchen)
   - soft (Warnings)
   - forbidden (harte Fehler)

7. Ergebnis:
   - PASS / WARNING / FAIL

---

## 📄 Expectations (Testdefinition)

Für jedes Dokument existiert ein JSON-File in:

tests/onboarding_expectations/

### Struktur

- document_reference → nur Kontext (kein doc_id!)
- match → identifiziert Dokument
- doc_id_rules → validiert doc_id
- registry_expectation:
  - strict → muss exakt passen
  - soft → sollte passen
  - forbidden → darf nicht auftreten

---

## ⚠️ Wichtige Design-Regeln

### 1. doc_id ≠ Erwartung

doc_id wird NICHT im Template fest verdrahtet.

Matching erfolgt über:
- Pattern
- Titel
- Datei

---

### 2. Template Generator (V5)

- übernimmt KEIN doc_id mehr
- generiert Pattern aus doc_id (Thema + Jahr)
- erzeugt keine widersprüchlichen Regeln

---

### 3. Trennung der Verantwortlichkeiten

| Komponente | Aufgabe |
|----------|--------|
| Classifier | LLM Output |
| Governance | Regeln |
| Config | Steuerung |
| Validator | Testlogik |

---

### 4. Normalisierung vor Governance

LLM Outputs werden normalisiert (z. B. confidence):

"high" → 0.9

---

## 🎯 Ziel des Setups

- Regression Testing für Onboarding
- Sicherstellen, dass neue Dokumente keine bestehenden brechen
- Transparente Qualitätsbewertung

---

## 📈 Nächster Schritt

- Mehrere Dokumente onboarden
- Regression über mehrere Expectations testen
- Retrieval-Qualität evaluieren