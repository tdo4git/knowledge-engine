# Strategic Knowledge Engine – Architecture
Version: 3.0

## Dokumentstatus

Titel: Strategic Knowledge Engine Architecture  
Layer: Architecture Layer  
Version: 3.0

Dieses Dokument ersetzt die Architekturdefinition v2.

---

# 1 Zielbild

Die Strategic Knowledge Engine ist ein mehrschichtiges Wissenssystem.

Sie trennt klar:

Document Sources  
Knowledge Construction  
Knowledge Base  
Knowledge Engine  
Bots

---

# 2 Systemarchitektur

Systemstruktur:

knowledge-engine/

knowledge_core  
knowledge_construction  
knowledge_base  
bots  
knowledge_sources

---

# 3 Knowledge Sources

Knowledge Sources enthalten Originaldokumente.

knowledge_sources/

intake  
archive  
raw_sensitive

---

# 4 Knowledge Construction

Knowledge Construction erzeugt die Wissensbasis.

Aufgaben:

- Dokumentanalyse
- Metadatenextraktion
- Registry-Erstellung
- Chunking
- Embedding-Erzeugung
- Indexaufbau

Diese Pipeline ist engine-spezifisch.

---

# 5 Knowledge Base

Die Knowledge Base enthält strukturierte Wissensartefakte:

registry  
chunks  
vector_index

Diese Artefakte werden durch Knowledge Construction erzeugt.

---

# 6 Knowledge Engine

Die Engine implementiert die Wissenslogik.

Pipeline:

Query  
→ Intent Engine  
→ Role Engine  
→ Retrieval Engine  
→ Scoring Engine  
→ Perspective Orchestrator  
→ Prompt Governance  
→ LLM

---

# 7 Bots

Bots sind Anwendungen auf der Engine.

Beispiele:

Trusted Advisor Bot  
Marketing Bot  
Insurance Portfolio Bot

Bots unterscheiden sich durch:

- Prompting
- Tonalität
- Use Case