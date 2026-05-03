import json
from pathlib import Path
import sys

BASE_PATH = Path(__file__).resolve().parent.parent
EXPECTATION_DIR = BASE_PATH / "tests/onboarding_expectations"


# -------------------------
# LOAD
# -------------------------
def load_expectations():
    files = list(EXPECTATION_DIR.glob("*.json"))

    data = []
    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            content = json.load(file)
            content["_file"] = f  # internal only
            data.append(content)

    return data


def get_review_items(expectations):
    return [e for e in expectations if e.get("review_required")]


# -------------------------
# HELPERS
# -------------------------
def save_item(item):
    path = item["_file"]

    # ❗ remove runtime field
    item_to_save = {k: v for k, v in item.items() if k != "_file"}

    with open(path, "w", encoding="utf-8") as f:
        json.dump(item_to_save, f, indent=2)


# -------------------------
# COMMANDS
# -------------------------
def list_reviews():
    expectations = load_expectations()
    reviews = get_review_items(expectations)

    print("\n=== REVIEW ITEMS ===\n")

    for i, e in enumerate(reviews):
        print(f"[{i}] {e.get('name')}")
        print(f"    mismatches: {e.get('mismatches')}")
        print()

    if not reviews:
        print("No open reviews.\n")


def show_review(index):
    reviews = get_review_items(load_expectations())

    try:
        item = reviews[index]
    except:
        print("Invalid index")
        return

    print("\n=== REVIEW DETAIL ===\n")
    print(json.dumps({k: v for k, v in item.items() if k != "_file"}, indent=2))


def diff_review(index):
    reviews = get_review_items(load_expectations())

    try:
        item = reviews[index]
    except:
        print("Invalid index")
        return

    reg = item.get("registry_expectation", {})
    ai = item.get("ai_suggestion", {})

    print("\n=== DIFF ===\n")

    for section in ["strict", "soft"]:
        for key in reg.get(section, {}):
            reg_val = reg[section].get(key)
            ai_val = ai.get(section, {}).get(key)

            status = "✔" if reg_val == ai_val else "❌"

            print(f"{status} {key}")
            print(f"   Registry: {reg_val}")
            print(f"   AI:       {ai_val}")

    print()


def accept_review(index):
    reviews = get_review_items(load_expectations())

    try:
        item = reviews[index]
    except:
        print("Invalid index")
        return

    # apply AI
    item["registry_expectation"] = item["ai_suggestion"]
    item["review_required"] = False
    item["source"] = "ai_accepted"

    item.pop("ai_suggestion", None)
    item.pop("mismatches", None)

    save_item(item)

    print("✅ AI suggestion accepted")


def reject_review(index):
    reviews = get_review_items(load_expectations())

    try:
        item = reviews[index]
    except:
        print("Invalid index")
        return

    item["review_required"] = False
    item["source"] = "registry_confirmed"

    item.pop("ai_suggestion", None)
    item.pop("mismatches", None)

    save_item(item)

    print("❌ AI suggestion rejected")


# -------------------------
# CLI ENTRY
# -------------------------
def main():

    if len(sys.argv) < 2:
        print("Usage:")
        print("  list")
        print("  show <id>")
        print("  diff <id>")
        print("  accept <id>")
        print("  reject <id>")
        return

    cmd = sys.argv[1]

    if cmd == "list":
        list_reviews()

    elif cmd == "show":
        show_review(int(sys.argv[2]))

    elif cmd == "diff":
        diff_review(int(sys.argv[2]))

    elif cmd == "accept":
        accept_review(int(sys.argv[2]))

    elif cmd == "reject":
        reject_review(int(sys.argv[2]))

    else:
        print("Unknown command")


if __name__ == "__main__":
    main()