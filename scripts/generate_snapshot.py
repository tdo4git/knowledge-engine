"""
generate_snapshot.py

Erzeugt einen kompakten System-Snapshot für den Claude-Kontext.
Output: knowledge_base/audit/snapshot.txt

Usage:
    python -m scripts.generate_snapshot
"""

import json
import faiss
from pathlib import Path
from datetime import datetime
from collections import Counter

# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_PATH = Path(__file__).resolve().parent.parent

REGISTRY_PATH  = BASE_PATH / "knowledge_base/registry/document_registry.json"
CHUNKS_PATH    = BASE_PATH / "knowledge_base/chunks/chunks.json"
FAISS_PATH     = BASE_PATH / "knowledge_base/vector_index/index.faiss"
CHUNK_IDS_PATH = BASE_PATH / "knowledge_base/vector_index/chunk_ids.json"
AUDIT_LOG_PATH = BASE_PATH / "knowledge_base/audit/onboarding_audit_log.jsonl"
INTAKE_PATH    = BASE_PATH / "knowledge_sources/intake"
ARCHIVE_PATH   = BASE_PATH / "knowledge_sources/archive"
OUTPUT_PATH    = BASE_PATH / "knowledge_base/audit/snapshot.txt"


# --------------------------------------------------
# LOADERS
# --------------------------------------------------

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_jsonl(path, last_n=10):
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    return [json.loads(l) for l in lines[-last_n:]]


# --------------------------------------------------
# SECTIONS
# --------------------------------------------------

def section_knowledge_base(registry, chunks):
    lines = ["## Knowledge Base"]

    # Counts
    lines.append(f"Dokumente : {len(registry)}")
    lines.append(f"Chunks    : {len(chunks)}")

    # FAISS
    try:
        index = faiss.read_index(str(FAISS_PATH))
        lines.append(f"FAISS     : {index.ntotal} entries")
        consistent = (index.ntotal == len(chunks))
        lines.append(f"Konsistenz: {'✔ OK' if consistent else '⚠ MISMATCH'}")
    except Exception as e:
        lines.append(f"FAISS     : ⚠ nicht lesbar ({e})")

    return lines


def section_registry(registry):
    lines = ["", "## Registry — Dokumente nach Origin"]

    by_origin = Counter(d.get("origin", "unknown") for d in registry)
    for origin, count in sorted(by_origin.items(), key=lambda x: -x[1]):
        lines.append(f"  {origin:<30} {count}")

    lines.append("")
    lines.append("## Registry — Dokumente nach Document Type")
    by_type = Counter(d.get("document_type", "unknown") for d in registry)
    for doc_type, count in sorted(by_type.items(), key=lambda x: -x[1]):
        lines.append(f"  {doc_type:<30} {count}")

    lines.append("")
    lines.append("## Registry — Alle Dokumente")
    lines.append(f"{'Doc-ID':<45} {'Origin':<25} {'Type':<25} {'Domain'}")
    lines.append("-" * 130)
    for d in registry:
        lines.append(
            f"{d.get('doc_id','?'):<45} "
            f"{d.get('origin','?'):<25} "
            f"{d.get('document_type','?'):<25} "
            f"{d.get('knowledge_domain','?')}"
        )

    return lines


def section_intake():
    lines = ["", "## Intake (ausstehend)"]

    if not INTAKE_PATH.exists():
        lines.append("  (Verzeichnis nicht gefunden)")
        return lines

    files = [f for f in INTAKE_PATH.iterdir() if f.is_file() and not f.name.startswith(".")]
    if not files:
        lines.append("  ✔ Leer — keine Dokumente ausstehend")
    else:
        lines.append(f"  {len(files)} Dokument(e) ausstehend:")
        for f in sorted(files):
            lines.append(f"  - {f.name}")

    return lines


def section_archive():
    lines = ["", "## Archive"]

    if not ARCHIVE_PATH.exists():
        lines.append("  (Verzeichnis nicht gefunden)")
        return lines

    files = [f for f in ARCHIVE_PATH.iterdir() if f.is_file() and not f.name.startswith(".")]
    lines.append(f"  {len(files)} Dokument(e) archiviert")

    return lines


def section_audit(audit_log_path, last_n=5):
    lines = ["", f"## Audit Log — letzte {last_n} Einträge"]

    if not audit_log_path.exists():
        lines.append("  (kein Audit Log gefunden)")
        return lines

    try:
        entries = load_jsonl(audit_log_path, last_n=last_n)
        for e in entries:
            ts = e.get("timestamp", "?")[:19]
            doc_id = e.get("doc_id", "?")
            origin = e.get("classification", {}).get("origin", "?")
            review = "⚠ REVIEW" if e.get("review", {}).get("review_required") else "✔"
            lines.append(f"  {ts}  {doc_id:<45} {origin:<20} {review}")
    except Exception as ex:
        lines.append(f"  ⚠ Fehler beim Lesen: {ex}")

    return lines


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("Generating snapshot...")

    # Load
    registry = load_json(REGISTRY_PATH)
    chunks   = load_json(CHUNKS_PATH)

    # Build
    output_lines = [
        "=" * 70,
        "STRATEGIC KNOWLEDGE ENGINE — SYSTEM SNAPSHOT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 70,
    ]

    output_lines += section_knowledge_base(registry, chunks)
    output_lines += section_registry(registry)
    output_lines += section_intake()
    output_lines += section_archive()
    output_lines += section_audit(AUDIT_LOG_PATH)

    output_lines += ["", "=" * 70]

    output = "\n".join(output_lines)

    # Save
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(output, encoding="utf-8")

    print(output)
    print(f"\nSaved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
    