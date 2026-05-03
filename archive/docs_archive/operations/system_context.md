# System Context – Strategic Knowledge Engine

## Zweck

Dieses Dokument definiert den operativen Nutzungskontext der Strategic Knowledge Engine.

Es ergänzt die Architektur-Dokumentation um die Perspektive:
→ Wie wird das System korrekt verwendet (insbesondere im Chat-Kontext)?

---

# 1. Grundprinzip

Die Knowledge Engine ist ein strukturiertes, mehrschichtiges System:

Document Sources  
→ Knowledge Construction  
→ Knowledge Base  
→ Knowledge Engine  
→ Bots

Wissen entsteht ausschließlich durch diese Pipeline.

---

# 2. Trennung von Wissen und Nutzung

Wichtig:

Wissen liegt in:
- Dokumentation
- Knowledge Base
- Config (Python)

Ein Chat hat keinen automatischen Zugriff auf dieses Wissen.

---

# 3. Chat-Kontext

Ein neuer Chat startet ohne:

- Architekturverständnis
- Retrieval-Logik
- Governance-Kontext
- Taxonomie

Daher muss ein System-Kontext bereitgestellt werden.

---

# 4. System Context Loader

Der Loader erfüllt folgende Funktion:

- selektiert relevante Informationen aus dem Projekt
- reduziert sie auf entscheidungsrelevanten Kontext
- stellt sie für den Chat bereit

Der Loader erzeugt kein Wissen, sondern nutzt bestehende Quellen.

---

# 5. Script Execution

Alle Skripte werden als Module gestartet:

python -m scripts.<script_name>

Beispiel:

python -m scripts.reset_knowledge_base

Voraussetzung:

- Ausführung im Verzeichnis: knowledge-engine/

---

# 6. Pfadlogik

BASE_PATH entspricht dem Projekt-Root:

knowledge-engine/

Empfohlen:

BASE_PATH = Path(__file__).resolve().parent.parent

Skripte dürfen nicht vom aktuellen Working Directory abhängen.

---

# 7. Taxonomie

Die Taxonomie ist:

- strikt definiert
- in Python Config implementiert
- Single Source of Truth

Wichtig:

- nur definierte Werte sind erlaubt
- keine freien Klassifikationen

---

# 8. Retrieval-Prinzipien

Das System verwendet:

- semantisches Retrieval (Vektorindex)
- dokumentzentrierte Aggregation
- governance-basierte Bewertung

Ranking basiert auf:

- semantischer Ähnlichkeit
- Herkunft (origin)
- Confidence
- Dokumenttyp

---

# 9. Kontextkonstruktion

Der Kontext für das LLM wird:

- aus mehreren Dokumenten aufgebaut
- bewusst begrenzt

Typisch:

- max_documents = 5
- max_chunks_per_document = 2

Ziel:

→ ausgewogener, nicht verzerrter Kontext

---

# 10. Governance

Grundsatz:

Das LLM erzeugt keine neuen Fakten.

Es verarbeitet ausschließlich:

- bereitgestellten Kontext
- selektierte Dokumente

---

# 11. Wichtiger Unterschied

Verfügbarkeit von Wissen ≠ Nutzung im Chat

Ein Dokument im Projekt bedeutet nicht,
dass es im Chat berücksichtigt wird.

---

# 12. Operational Modes

Der Loader unterstützt verschiedene Modi:

expert:
→ Fokus auf Architektur und Strategie und Diskussion

onboarding:
→ Fokus auf Knowledge Construction

debug:
→ Fokus auf Retrieval und Pipeline

coding:
→ vollständige Taxonomie und Config für Code-Erzeugung

---

# 13. Ziel dieses Dokuments

Dieses Dokument stellt sicher, dass:

- jeder Chat mit korrektem Systemverständnis startet
- keine impliziten Annahmen entstehen
- das System konsistent genutzt wird