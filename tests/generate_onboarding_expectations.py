from pathlib import Path
import json
import re

BASE_PATH = Path(__file__).resolve().parent.parent

REGISTRY_PATH = BASE_PATH / "knowledge_base/registry/document_registry.json"
OUTPUT_DIR = BASE_PATH / "tests/onboarding_expectations"


# -------------------------
# HELPERS
# -------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sanitize_filename(name):
    name = name.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"\s+", "_", name)
    return name


def generate_doc_id_pattern(doc_id):
    """
    Generalisiert doc_id für Pattern-Matching
    """
    parts = doc_id.split("_")

    # Beispiel: doc_legislator_EU_dora_verordnung_eu_2022_2554
    # → wir behalten nur Jahr + evtl. letzten Teil
    if len(parts) > 2:
        return f"doc_*_{parts[-2]}"

    return doc_id


def extract_strict_fields(doc):
    return {
        "document_type": doc.get("document_type"),
        "origin": doc.get("origin"),
        "jurisdiction": doc.get("jurisdiction")
    }


def extract_soft_fields(doc):
    return {
        "knowledge_domain": doc.get("knowledge_domain"),
        "domain_layer": doc.get("domain_layer")
    }


def extract_forbidden_fields(doc):
    forbidden = {}

    # Beispielregel: misc ist nie erlaubt
    if doc.get("knowledge_domain") == "misc":
        forbidden["knowledge_domain"] = ["misc"]

    return forbidden


# -------------------------
# MAIN
# -------------------------
def main():
    print("\n=== GENERATE EXPECTATIONS ===\n")

    registry = load_json(REGISTRY_PATH)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for doc in registry:
        title = doc.get("title", "document")
        filename = sanitize_filename(title)

        expectation = {
            "name": title,
            "match": {
                "doc_id_pattern": generate_doc_id_pattern(doc["doc_id"])
            },
            "registry_expectation": {
                "strict": extract_strict_fields(doc),
                "soft": extract_soft_fields(doc),
                "forbidden": extract_forbidden_fields(doc)
            }
        }

        output_path = OUTPUT_DIR / f"{filename}.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(expectation, f, indent=2)

        print(f"✔ Generated: {output_path}")


if __name__ == "__main__":
    main()