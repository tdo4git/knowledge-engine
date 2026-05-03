# Repository Map -- Strategic Knowledge Engine

## Purpose

This document provides a quick orientation guide for the repository. It
explains the purpose of each top‑level directory and the main components
of the Strategic Knowledge Engine.

The goal is that new developers can understand the structure of the
project within a few minutes.

------------------------------------------------------------------------

# Repository Structure

project-root/

knowledge-bot-mvp/\
knowledge-engine/

------------------------------------------------------------------------

# 1 knowledge-bot-mvp

This directory contains the **original MVP implementation** of the
Knowledge Bot.

Purpose:

-   historical reference
-   early prototype implementation
-   comparison with the new architecture

The MVP is not the main development focus anymore but remains useful for
reference and experimentation.

------------------------------------------------------------------------

# 2 knowledge-engine

This directory contains the **Strategic Knowledge Engine**, which
represents the new architecture of the system.

It includes:

-   the knowledge engine
-   the knowledge construction pipeline
-   the generated knowledge base
-   the bots using the engine
-   the document sources

Structure:

knowledge-engine/

    knowledge_core/
    knowledge_construction/
    knowledge_base/
    bots/
    knowledge_sources/
    config/
    notebooks/
    docs/

------------------------------------------------------------------------

# 2.1 knowledge_core

The **core engine implementation**.

This module implements the reasoning pipeline that processes user
queries.

Typical components:

-   Intent Engine
-   Role Engine
-   Retrieval Engine
-   Scoring Engine
-   Perspective Orchestrator
-   Prompt Governance
-   Query Pipeline

Location:

knowledge-engine/knowledge_core

------------------------------------------------------------------------

# 2.2 knowledge_construction

The **document processing and knowledge creation pipeline**.

This module transforms raw documents into structured knowledge
artifacts.

Responsibilities:

-   metadata extraction
-   registry creation
-   document chunking
-   embedding generation
-   vector index creation

Location:

knowledge-engine/knowledge_construction

------------------------------------------------------------------------

# 2.3 knowledge_base

The generated **structured knowledge base** used by the engine.

Artifacts:

registry/ chunks/ vector_index/

These artifacts are produced by the knowledge construction pipeline.

Location:

knowledge-engine/knowledge_base

------------------------------------------------------------------------

# 2.4 bots

Applications built on top of the knowledge engine.

Each bot defines:

-   prompts
-   tone and style
-   application logic

Example bots:

-   trusted_advisor_bot
-   marketing_bot
-   insurance_portfolio_bot

Location:

knowledge-engine/bots

------------------------------------------------------------------------

# 2.5 knowledge_sources

Original documents used to build the knowledge base.

Structure:

knowledge_sources/

    intake/
    archive/
    raw_sensitive/

Description:

intake\
Dropzone for new documents.

archive\
Curated original documents included in the knowledge base.

raw_sensitive\
Internal or sensitive documents.

Location:

knowledge-engine/knowledge_sources

------------------------------------------------------------------------

# 2.6 config

Configuration files for the knowledge engine.

Examples:

-   engine configuration
-   retrieval parameters
-   model settings

Location:

knowledge-engine/config

------------------------------------------------------------------------

# 2.7 notebooks

Jupyter notebooks used for experimentation and analysis.

Typical uses:

-   retrieval experiments
-   embedding evaluation
-   debugging

Location:

knowledge-engine/notebooks

------------------------------------------------------------------------

# 2.8 docs

Project documentation.

Typical contents:

-   architecture documentation
-   governance rules
-   system overview
-   architecture diagrams

Location:

knowledge-engine/docs

------------------------------------------------------------------------

# Development Philosophy

The repository follows several architectural principles:

1.  Clear separation of documents and knowledge
2.  Separation of knowledge construction and knowledge usage
3.  A central knowledge engine used by multiple bots
4.  Full traceability of the knowledge base
5.  Modular architecture enabling future extensions

------------------------------------------------------------------------

# Summary

The repository separates:

Document Sources\
→ Knowledge Construction\
→ Knowledge Base\
→ Knowledge Engine\
→ Bots

This structure enables explainable, maintainable, and extensible
knowledge systems.
