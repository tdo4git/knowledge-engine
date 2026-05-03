from pathlib import Path
import importlib
import argparse

# --------------------------------------------------
# Start with: python -m scripts.system_context_loader --mode xxxxx
# --------------------------------------------------

# --------------------------------------------------
# BASE PATH
# --------------------------------------------------

BASE_PATH = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# CONFIG IMPORTS (Single Source of Truth)
# --------------------------------------------------

taxonomy = importlib.import_module("config.taxonomy")
scoring = importlib.import_module("config.scoring_config")
engine = importlib.import_module("config.engine_config")

# --------------------------------------------------
# CONTEXT MODES
# --------------------------------------------------

CONTEXT_MODES = {
    "default": {
        "docs": [
            "docs/operations/working_style.md",
            "docs/operations/system_context.md",
            "docs/architecture/system/architecture_overview_v3.md",
            "docs/architecture/engine/retrieval_architecture_guideline.md",
            "docs/governance/explainability_principles.md",
        ],
        "taxonomy": "summary",
        "scoring": "summary"
    },
    "onboarding": {
        "docs": [
            "docs/operations/onboarding_working_style.md",
            "docs/operations/system_context.md",            
            "docs/architecture/system/architecture_overview_v3.md",
            "docs/architecture/knowledge/knowledge_construction_pipeline.md",
            "docs/architecture/knowledge/knowledge_base_schema.md",
            "docs/governance/explainability_principles.md",
            "REPOSITORY_MAP",        ],
        "taxonomy": "full",
        "scoring": "full"
    },
    "debug": {
        "docs": [
            "docs/operations/working_style.md",
            "docs/operations/system_context.md",    
            "docs/architecture/engine/retrieval_architecture_guideline.md",
            "docs/query_execution_pipeline.md",
        ],
        "taxonomy": "summary",
        "scoring": "full"
    },
    "retrieval_test": {
        "docs": [
            "docs/operations/working_style.md",
            "docs/operations/system_context.md",    
            "docs/operations/query_execution.md",    
            "docs/architecture/engine/retrieval_architecture_guideline.md",
            "docs/architecture/query_execution_pipeline.md",
            "docs/governance/explainability_principles.md",
        ],
        "taxonomy": "full",
        "scoring": "full"
    },
    "coding": {
        "docs": [
            "docs/operations/working_style.md",
            "docs/operations/system_context.md",
            "docs/operations/query_execution.md",        
            "docs/architecture/system/architecture_overview_v3.md",
            "docs/architecture/engine/retrieval_architecture_guideline.md",
            "REPOSITORY_MAP",
        ],
        "taxonomy": "full", 
        "scoring": "full"
    },
    "expert": {
        "docs": [
            "docs/operations/working_style.md",
            "docs/operations/system_context.md",    
            "docs/architecture/system/architecture_overview_v3.md",
            "docs/architecture/engine/retrieval_architecture_guideline.md",
            "docs/query_execution_pipeline.md",
            "docs/governance/explainability_principles.md",
            "REPOSITORY_MAP",
        ],
        "taxonomy": "full",
        "scoring": "full"
    }
}

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def read_doc(path):
    if not path.exists():
        return f"[MISSING: {path}]"
    return path.read_text(encoding="utf-8")[:1500]

def load_repo_map():
    from scripts.generate_repo_map import build_tree
    return build_tree(BASE_PATH)

def save_context(prompt, mode):
    output_path = BASE_PATH / f"chat_context_{mode}.txt"
    output_path.write_text(prompt, encoding="utf-8")
    print(f"\nSaved to: {output_path}")

# --------------------------------------------------
# FORMATTERS
# --------------------------------------------------

def format_taxonomy(mode):
    if mode == "summary":
        return "\nTaxonomy: fixed categories defined in system config."

    lines = ["\n=== TAXONOMY (STRICT) ==="]

    for name in [
        "DOCUMENT_TYPES",
        "DOMAIN_LAYERS",
        "KNOWLEDGE_DOMAINS",
        "TOPICS",
        "ORIGINS",
        "JURISDICTIONS"
    ]:
        values = getattr(taxonomy, name, None)
        if values:
            lines.append(f"\n{name}:")
            for v in values:
                lines.append(f"- {v}")

    return "\n".join(lines)


def format_scoring(mode):
    if mode == "summary":
        return "\nScoring: governance-aware ranking (origin, confidence, document type)."

    cfg = scoring.SCORING_CONFIG

    lines = ["\n=== SCORING MODEL ==="]

    lines.append("\nOrigin Weights:")
    for k, v in cfg["origin_weights"].items():
        lines.append(f"- {k}: {v}")

    lines.append("\nConfidence Weights:")
    for k, v in cfg["confidence_weights"].items():
        lines.append(f"- {k}: {v}")

    lines.append("\nDocument Type Weights:")
    for k, v in cfg["document_type_weights"].items():
        lines.append(f"- {k}: {v}")

    return "\n".join(lines)


def format_engine():
    cfg = engine.RETRIEVAL_CONFIG
    context = cfg["context_construction"]

    return f"""
=== RETRIEVAL CONTEXT ===
max_documents: {context['max_documents']}
max_chunks_per_document: {context['max_chunks_per_document']}
"""


# --------------------------------------------------
# CONTEXT BUILDER
# --------------------------------------------------

def build_context(mode):

    if mode not in CONTEXT_MODES:
        raise ValueError(f"Unknown mode: {mode}")

    cfg = CONTEXT_MODES[mode]

    parts = []

    # Docs
    for doc_path in cfg["docs"]:
        full_path = BASE_PATH / doc_path
        parts.append(f"\n=== {doc_path} ===\n{read_doc(full_path)}")

    for doc_path in cfg["docs"]:

        # 🔴 Sonderfall: dynamische Repo-Map
        if "REPOSITORY_MAP" in doc_path:
            parts.append("\n=== REPOSITORY STRUCTURE (LIVE) ===\n")
            parts.append(load_repo_map())
            continue

        # 🟢 Standardfall: Datei laden
        full_path = BASE_PATH / doc_path
        parts.append(f"\n=== {doc_path} ===\n{read_doc(full_path)}")

    # Taxonomy
    parts.append(format_taxonomy(cfg["taxonomy"]))

    # Scoring
    parts.append(format_scoring(cfg["scoring"]))

    # Engine config (always relevant)
    parts.append(format_engine())

    return "\n".join(parts)


def build_prompt(mode):
    context = build_context(mode)

    return f"""
Ich arbeite an einer Strategic Knowledge Engine.

System Context:
{context}

Arbeitsprinzipien:
- strikt entlang bestehender Architektur arbeiten
- keine ad-hoc Lösungen
- Governance und Explainability priorisieren
- keine workarounds, die nicht der architektur entsprechen
- erstelle immer vollständige Dateien, die ich 1:1 übernehmen kann
- Architektur-Brüche sind nicht erlaubt.

Mode: {mode}

Ziel dieses Chats:
[HIER EINTRAGEN]
"""


# --------------------------------------------------
# CLI
# --------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="expert",
                        choices=list(CONTEXT_MODES.keys()))

    args = parser.parse_args()

    prompt = build_prompt(args.mode)

    print(prompt)

    save_context(prompt, args.mode)

if __name__ == "__main__":
    main()