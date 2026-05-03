# Spielregeln – Knowledge Engine Governance
Version: 2.0

## Zweck dieses Dokuments

Dieses Dokument definiert die verbindlichen Governance-Regeln für Aufbau, Pflege und Nutzung der Strategic Knowledge Engine.

Ziel ist es, sicherzustellen:

- fachliche Qualität
- klare Verantwortlichkeiten
- nachvollziehbare Wissensherkunft
- reproduzierbare Wissensbasis

Die Governance gilt für alle Komponenten der Knowledge Engine.

---

# 1 Grundprinzipien

## 1.1 Trennung von Dokumenten und Wissen

Nicht jedes Dokument ist automatisch Wissen.

Wissen entsteht erst durch:

- bewusste Auswahl
- Metadatenzuordnung
- technische Verarbeitung

Der Lebenszyklus eines Dokuments ist:

Document Sources  
→ Knowledge Construction  
→ Knowledge Base  
→ Knowledge Engine  
→ Bot

---

## 1.2 Mensch entscheidet – Technik verarbeitet

Menschen entscheiden:

- welche Dokumente relevant sind
- welche Metadaten gelten
- welche Inhalte freigegeben werden

Technik übernimmt:

- Textextraktion
- Chunking
- Embeddings
- Retrieval

---

# 2 Verzeichnisstruktur

Die Knowledge Engine folgt folgender Systemstruktur:

project-root/

knowledge-bot-mvp/  
knowledge-engine/

---

## 2.1 Knowledge Sources

Originaldokumente liegen hier:

knowledge_engine/knowledge_sources

Struktur:

knowledge_sources/

intake/  
archive/  
raw_sensitive/

Bedeutung:

intake  
→ neue Dokumente werden hier abgelegt

archive  
→ kuratierte Originaldokumente

raw_sensitive  
→ interne oder vertrauliche Dokumente

---

## 2.2 Knowledge Construction

Der Wissensaufbau erfolgt hier:

knowledge_engine/knowledge_construction

Aufgaben:

- Metadatenextraktion
- Registry-Erstellung
- Chunking
- Embedding-Erzeugung
- Indexerstellung

---

## 2.3 Knowledge Base

Die generierte Wissensbasis liegt hier:

knowledge_engine/knowledge_base

Struktur:

knowledge_base/

registry/  
chunks/  
vector_index/

Diese Artefakte werden automatisch erzeugt.

---

## 2.4 Knowledge Engine

Die Engine liegt in:

knowledge_engine/knowledge_core

Komponenten:

Intent Engine  
Role Engine  
Retrieval Engine  
Scoring Engine  
Perspective Orchestrator  
Prompt Governance

---

## 2.5 Bots

Bots sind Anwendungen auf der Engine.

Sie liegen in:

knowledge_engine/bots

Beispiele:

trusted_advisor_bot  
marketing_bot  
insurance_portfolio_bot

Ein Bot nutzt immer dieselbe Engine und Knowledge Base.

---

# 3 Dokument-Lifecycle

Der vollständige Lifecycle eines Dokuments:

knowledge_sources/intake  
↓  
knowledge_sources/archive  
↓  
knowledge_construction  
↓  
knowledge_base  
↓  
knowledge_engine  
↓  
bot

---

# 4 Metadaten

Metadaten werden in der Registry gespeichert.

Pflichtfelder:

doc_id  
file_path  
origin  
role  
themes  
year  
trust_level  
text_quality

Metadaten ermöglichen:

- Retrievalfilter
- Scoring
- Perspektivensteuerung
- Explainability