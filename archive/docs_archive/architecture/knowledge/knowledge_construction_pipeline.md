# Knowledge Construction Pipeline

*(Strategic Knowledge Engine V3)*

## 1. Ziel der Knowledge Construction Pipeline

Die Knowledge Construction Pipeline ist verantwortlich für den Aufbau
und die Aktualisierung der Knowledge Base. Sie transformiert
unstrukturierte Dokumente in eine strukturierte, durchsuchbare
Wissensbasis.

Prozessübersicht:

document → metadata extraction → classification → governance validation
→ registry entry → text extraction → chunking → embeddings → vector
index

Ergebnis: eine persistente Knowledge Base, die durch die Retrieval
Engine abgefragt werden kann.

------------------------------------------------------------------------

# 2. Architekturüberblick

## 2.1 Dokument-Onboarding

document\
→ preview_extractor\
→ classifier (LLM)\
→ governance rules\
→ governance review\
→ validation\
→ registry update\
→ text extraction\
→ chunking\
→ audit logging

## 2.2 Knowledge Base Update

chunks.json\
→ embedding generation (incremental)\
→ FAISS index update\
→ consistency check

------------------------------------------------------------------------

# 3. Pipeline-Komponenten

## 3.1 Preview Extractor

Modul: knowledge_construction/metadata/preview_extractor.py

Aufgabe: Extrahiert einen kurzen Dokumentausschnitt (\~6000 Zeichen) zur
Klassifikation.

------------------------------------------------------------------------

## 3.2 Document Classifier

Modul: knowledge_construction/metadata/classifier.py

Bestimmte Felder:

-   document_type
-   domain_layer
-   knowledge_domain
-   origin
-   jurisdiction
-   confidence

------------------------------------------------------------------------

## 3.3 Governance Layer

Deterministische Regeln korrigieren typische LLM-Fehler.

Beispiele: BaFin → supervisory_authority\
AWS → cloud_vendor

Module:

-   governance_rules.py
-   governance.py

------------------------------------------------------------------------

## 3.4 Validation Layer

Module:

-   validation/validation.py
-   validation/cross_field_rules.py

Validierung:

Enum Validation -- prüft erlaubte Werte\
Cross Field Validation -- prüft Feldkonsistenz

Taxonomien definiert in:

config/taxonomy.py

------------------------------------------------------------------------

## 3.5 Registry Builder

Modul: knowledge_construction/registry/registry_builder.py

Artefakt:

knowledge_base/registry/document_registry.json

------------------------------------------------------------------------

## 3.6 Document Text Extraction

Modul:

knowledge_construction/document_processing/document_text_extractor.py

Unterstützte Formate:

-   PDF
-   DOCX
-   TXT

------------------------------------------------------------------------

## 3.7 Chunking

Modul:

knowledge_construction/chunking/chunker.py

Chunk Eigenschaften:

-   chunk_id
-   doc_id
-   chunk_index
-   text
-   tokens
-   token_start
-   token_end

Parameter (config/construction_config.py):

-   CHUNK_SIZE
-   CHUNK_OVERLAP

------------------------------------------------------------------------

## 3.8 Audit Logging

Modul:

knowledge_construction/audit/audit_logger.py

Artefakt:

knowledge_base/audit/onboarding_audit_log.jsonl

------------------------------------------------------------------------

# 4. Embedding Pipeline

Modul:

knowledge_construction/embedding/embedding_generator.py

Embedding Modell:

sentence-transformers/all-MiniLM-L6-v2

Speicherort:

knowledge_base/vector_index/embeddings.pt

------------------------------------------------------------------------

# 5. Incremental Embedding

Neue Chunks werden erkannt über:

vector_index/chunk_ids.json

Workflow:

chunks.json\
→ finde neue chunks\
→ embedde nur neue chunks\
→ erweitere embeddings\
→ erweitere FAISS index

------------------------------------------------------------------------

# 6. FAISS Vector Index

Artefakt:

knowledge_base/vector_index/index.faiss

Index-Typ:

IndexFlatL2

------------------------------------------------------------------------

# 7. Index Consistency Check

Modul:

knowledge_construction/embedding/index_consistency_check.py

Synchronisierte Artefakte:

-   chunks.json
-   embeddings.pt
-   chunk_ids.json
-   index.faiss

------------------------------------------------------------------------

# 8. Knowledge Base Artefakte

knowledge_base/

registry/ document_registry.json

chunks/ chunks.json

vector_index/ embeddings.pt chunk_ids.json index.faiss

audit/ onboarding_audit_log.jsonl

------------------------------------------------------------------------

# 9. Onboarding Workflow

OnboardingPipeline.process_document()

Ablauf:

document\
→ preview extraction\
→ classification\
→ governance\
→ validation\
→ registry entry\
→ text extraction\
→ chunking\
→ embedding update\
→ index update\
→ consistency check\
→ audit log

------------------------------------------------------------------------

# 10. Ergebnis

Die Construction Pipeline erzeugt eine strukturierte Knowledge Base, die
durch die Retrieval Engine abgefragt werden kann.


## Erweiterung: Governance & Review Layer

Nach der initialen Klassifikation und Validierung wurde ein zusätzlicher Review-Mechanismus eingeführt.

### Review Decision

Die Pipeline enthält nun eine nicht-blockierende Qualitätsbewertung:

- review_required (bool)
- review_reasons (list)

Ziel:

- automatische Verarbeitung beibehalten
- kritische Dokumente markieren
- spätere manuelle Prüfung ermöglichen

Die Review-Logik basiert auf:

- Confidence-Wert
- Dokumenttyp (z. B. regulatorisch)
- Klassifikationsqualität

Wichtig:

Die Review-Entscheidung blockiert die Pipeline nicht, sondern ergänzt die Metadaten.


Update am 20.03.2026:

## Knowledge Construction Pipeline (Updated)

The knowledge construction pipeline follows a structured, governance-driven process:

1. Classification (LLM, contract-driven)
   - Uses YAML-based prompt contracts
   - Prompt Builder generates system + user prompt
   - LLM returns structured JSON

2. Governance Pipeline (centralized)
   - apply_governance()
   - origin normalization
   - jurisdiction rules
   - bias derivation
   - confidence calculation

3. Validation
   - enum validation
   - cross-field validation

4. Registry persistence
   - document metadata stored

5. Chunking
   - token-based segmentation

6. Embeddings
   - vector generation

7. Indexing
   - FAISS index update

RULE:
All governance logic must pass through the governance pipeline.
No distributed logic allowed.