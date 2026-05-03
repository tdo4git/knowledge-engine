# Strategic Knowledge Engine -- Architecture Diagram

Dieses Dokument zeigt die Architektur der Strategic Knowledge Engine als
Übersichtsgrafik.

Die Architektur folgt der Struktur:

Document Sources → Knowledge Construction → Knowledge Base → Knowledge
Engine → Bots

------------------------------------------------------------------------

## System Architecture

``` mermaid
flowchart LR

    subgraph Sources["Document Sources"]
        A1[intake]
        A2[archive]
        A3[raw_sensitive]
    end

    subgraph Construction["Knowledge Construction"]
        B1[Metadata Extraction]
        B2[Registry Builder]
        B3[Chunker]
        B4[Embedding Generator]
    end

    subgraph KnowledgeBase["Knowledge Base"]
        C1[Document Registry]
        C2[Chunks]
        C3[Vector Index]
    end

    subgraph Engine["Knowledge Engine (knowledge_core)"]
        D1[Intent Engine]
        D2[Role Engine]
        D3[Retrieval Engine]
        D4[Scoring Engine]
        D5[Perspective Orchestrator]
        D6[Prompt Governance]
        D7[LLM]
    end

    subgraph Bots["Bots"]
        E1[Trusted Advisor Bot]
        E2[Marketing Bot]
        E3[Insurance Portfolio Bot]
    end

    A1 --> A2
    A2 --> B1

    B1 --> B2
    B2 --> B3
    B3 --> B4

    B2 --> C1
    B3 --> C2
    B4 --> C3

    C1 --> D3
    C2 --> D3
    C3 --> D3

    D1 --> D2
    D2 --> D3
    D3 --> D4
    D4 --> D5
    D5 --> D6
    D6 --> D7

    D7 --> E1
    D7 --> E2
    D7 --> E3
```

------------------------------------------------------------------------

## Architektur-Ebenen

### 1. Document Sources

Ordner: - knowledge_sources/intake - knowledge_sources/archive -
knowledge_sources/raw_sensitive

Diese enthalten die ursprünglichen Dokumente.

------------------------------------------------------------------------

### 2. Knowledge Construction

Pipeline für den Wissensaufbau: - Metadatenextraktion -
Registry-Erstellung - Dokument-Chunking - Embedding-Erzeugung - Aufbau
des Vektorindexes

------------------------------------------------------------------------

### 3. Knowledge Base

Bestandteile: - Document Registry - Chunks - Vector Index

Diese Artefakte werden automatisch durch die Construction Pipeline
erzeugt.

------------------------------------------------------------------------

### 4. Knowledge Engine

Pipeline:

Query → Intent Engine → Role Engine → Retrieval Engine → Scoring Engine
→ Perspective Orchestrator → Prompt Governance → LLM → Answer

------------------------------------------------------------------------

### 5. Bots

Beispiele: - trusted_advisor_bot - marketing_bot -
insurance_portfolio_bot

Bots unterscheiden sich durch Prompting, Tonalität und Use Case, greifen
aber auf dieselbe Engine und Knowledge Base zu.
