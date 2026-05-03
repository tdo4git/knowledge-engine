import json
from pathlib import Path
import subprocess
import sys

BASE_PATH = Path(__file__).resolve().parent.parent

REGISTRY_PATH = BASE_PATH / "knowledge_base/registry/document_registry.json"
EXPECTATION_DIR = BASE_PATH / "tests/onboarding_expectations"
AI_SUGGESTION_DIR = BASE_PATH / "tests/onboarding_ai_suggestions"

INTAKE_DIR = BASE_PATH / "knowledge_sources/intake"
ARCHIVE_DIR = BASE_PATH / "knowledge_sources/archive"

# ------------------------------------------------
# FLAGS
# ------------------------------------------------

APPLY_MODE = "--apply" in sys.argv
REGRESSION_MODE = "--regression" in sys.argv

IGNORE_FIELDS = {"confidence"}

# ------------------------------------------------
# COMMANDS
# ------------------------------------------------

def run_command(cmd):
    subprocess.run(cmd, check=True)


def reset_knowledge_base():
    print("🔄 Reset Knowledge Base (archive → intake)")
    run_command(["python", "-m", "scripts.reset_knowledge_base"])


def run_onboarding():
    print("🚀 Run Onboarding")
    run_command(["python", "-m", "scripts.run_onboarding"])


# ------------------------------------------------
# ARCHIVING
# ------------------------------------------------

def archive_document(source_file):
    source = INTAKE_DIR / source_file
    target = ARCHIVE_DIR / source_file

    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        source.rename(target)
        print(f"📦 Archived: {source_file}")


# ------------------------------------------------
# LOADERS
# ------------------------------------------------

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_registry():
    return load_json(REGISTRY_PATH)


def load_expectations():
    expectations = {}

    if not EXPECTATION_DIR.exists():
        return expectations

    for file in EXPECTATION_DIR.glob("*.json"):
        try:
            data = load_json(file)

            if "doc_id" not in data:
                print(f"⚠️ Invalid expectation: {file.name}")
                continue

            expectations[data["doc_id"]] = data

        except Exception as e:
            print(f"⚠️ Error loading {file.name}: {e}")

    return expectations


def load_ai():
    ai = {}

    if not AI_SUGGESTION_DIR.exists():
        return ai

    for file in AI_SUGGESTION_DIR.glob("*.json"):
        try:
            data = load_json(file)

            if "doc_id" not in data:
                continue

            ai[data["doc_id"]] = data.get("ai", {})

        except Exception:
            continue

    return ai


# ------------------------------------------------
# EXPECTATION
# ------------------------------------------------

def create_expectation(doc):
    return {
        "doc_id": doc["doc_id"],
        "title": doc["title"],
        "expected": {
            k: v for k, v in doc.items()
            if k not in ["doc_id", "title", "source_file"]
        },
        "status": "TO_REVIEW"
    }


def save_expectation(doc_id, data):
    EXPECTATION_DIR.mkdir(parents=True, exist_ok=True)
    path = EXPECTATION_DIR / f"{doc_id}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ------------------------------------------------
# COMPARISON
# ------------------------------------------------

def compare(doc, expected, ai):

    keys = set(doc.keys()) & set(expected.keys())

    if ai:
        keys = keys & set(ai.keys())

    keys = {k for k in keys if k not in IGNORE_FIELDS}

    result = {}

    for k in sorted(keys):
        result[k] = {
            "registry": doc.get(k),
            "expected": expected.get(k),
            "ai": ai.get(k) if ai else None
        }

    return result


# ------------------------------------------------
# DECISION
# ------------------------------------------------

def classify(values):
    r, e, a = values["registry"], values["expected"], values["ai"]

    if r == e:
        return "OK"

    if a is not None and a == e:
        return "SYSTEM_ERROR"

    if a is not None and a == r:
        return "EXPECTATION_OUTDATED"

    return "REVIEW"


def decision_symbol(decision):
    return {
        "OK": "✔",
        "SYSTEM_ERROR": "❌",
        "EXPECTATION_OUTDATED": "⚠",
        "REVIEW": "?"
    }[decision]


def has_relevant_difference(comp):
    return any(classify(v) != "OK" for v in comp.values())


# ------------------------------------------------
# OUTPUT
# ------------------------------------------------

def print_comparison(doc_id, comp):

    print("\n===================================")
    print(f"📄 {doc_id}")
    print("=== REGISTRY vs EXPECTATION vs AI ===")

    for field, values in comp.items():

        decision = classify(values)
        symbol = decision_symbol(decision)

        print(f"{symbol} {field}")
        print(f"   Registry:    {values['registry']}")
        print(f"   Expectation: {values['expected']}")
        print(f"   AI:          {values['ai']}")

    print("===================================\n")


# ------------------------------------------------
# MAIN
# ------------------------------------------------

def main():

    print("\n=== ONBOARDING VALIDATION V6.4 ===\n")
    print(f"Mode: {'APPLY' if APPLY_MODE else 'VALIDATE'}")
    print(f"Regression Mode: {'ON' if REGRESSION_MODE else 'OFF'}\n")

    if REGRESSION_MODE:
        reset_knowledge_base()

    run_onboarding()

    registry = load_registry()
    expectations = load_expectations()
    ai = load_ai()

    failures = 0
    reviews = 0
    created = 0
    archived = 0
    fixed = 0

    for doc in registry:

        doc_id = doc["doc_id"]
        source_file = doc["source_file"]

        exp = expectations.get(doc_id)
        ai_s = ai.get(doc_id, {})

        # ---------------------------
        # CREATE EXPECTATION
        # ---------------------------

        if not exp:
            new_exp = create_expectation(doc)
            save_expectation(doc_id, new_exp)

            print(f"🆕 Created expectation → {doc_id}")
            print(f"⚠ Keeping in intake\n")

            created += 1
            exp = new_exp

        # ---------------------------
        # COMPARISON (FIX!)
        # ---------------------------

        comp = compare(doc, exp["expected"], ai_s)

        if has_relevant_difference(comp) or exp.get("status") != "APPROVED":
            print_comparison(doc_id, comp)

        # ---------------------------
        # NOT APPROVED
        # ---------------------------

        if exp.get("status") != "APPROVED":
            print(f"⚠ {doc_id} → expectation not approved")
            print(f"⚠ Keeping in intake\n")

            reviews += 1
            continue

        # ---------------------------
        # DECISION LOOP
        # ---------------------------

        doc_has_error = False

        for field, values in comp.items():

            decision = classify(values)

            if decision == "SYSTEM_ERROR":
                failures += 1
                doc_has_error = True

            elif decision == "EXPECTATION_OUTDATED":
                if APPLY_MODE:
                    exp["expected"][field] = values["registry"]
                    fixed += 1

            elif decision == "REVIEW":
                reviews += 1

        # ---------------------------
        # ARCHIVE
        # ---------------------------

        if not doc_has_error:
            archive_document(source_file)
            archived += 1

        if APPLY_MODE and not doc_has_error:
            save_expectation(doc_id, exp)

    # ---------------------------
    # SUMMARY
    # ---------------------------

    print("\n===================================")
    print(f"Created:  {created}")
    print(f"Fixed:    {fixed}")
    print(f"Reviews:  {reviews}")
    print(f"Archived: {archived}")
    print(f"Failures: {failures}")
    print("===================================\n")

    if failures > 0:
        raise ValueError("❌ REGRESSION DETECTED")

    print("✔ VALIDATION PASSED\n")


if __name__ == "__main__":
    main()