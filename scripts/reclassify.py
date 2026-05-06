"""
TD-007 — Reklassifizierungs-Skript
====================================
Korrigiert Klassifikationsfelder in der Knowledge Base ohne vollständiges Re-Onboarding.

Unterstützte Korrekturen:
  document_type  → nur Registry-Update (doc_id und Chunks bleiben unverändert)
  origin         → Registry (neue doc_id) + Chunks + Vector Index reorder

Kein LLM-Aufruf — alle Korrekturen sind explizit im Patch-File definiert.

Usage:
    python -m scripts.reclassify --patch config/reclassify_patch.json
    python -m scripts.reclassify --patch config/reclassify_patch.json --dry-run

Patch-Format (JSON-Array):
[
  {
    "doc_id": "doc_supervisory_insurance_83c73b",
    "fields": {"document_type": "supervisory_guidance"}
  },
  {
    "doc_id": "doc_research_digitalesouver...",
    "fields": {"origin": "industry_association"}
  }
]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import faiss
import numpy as np
import torch

# ============================================================
# PATHS  (identisch mit anderen Scripts: BASE_PATH-Convention)
# ============================================================

BASE_PATH = Path(__file__).resolve().parent.parent

REGISTRY_PATH  = BASE_PATH / "knowledge_base/registry/document_registry.json"
CHUNKS_PATH    = BASE_PATH / "knowledge_base/chunks/chunks.json"
EMBEDDINGS_PATH = BASE_PATH / "knowledge_base/vector_index/embeddings.pt"
FAISS_INDEX_PATH = BASE_PATH / "knowledge_base/vector_index/index.faiss"
CHUNK_IDS_PATH = BASE_PATH / "knowledge_base/vector_index/chunk_ids.json"
AUDIT_LOG_PATH = BASE_PATH / "knowledge_base/audit/onboarding_audit_log.jsonl"

# ============================================================
# TAXONOMY VALIDATION
# ============================================================

VALID_FIELDS = {"document_type", "origin"}

VALID_VALUES = {
    "document_type": [
        "regulatory_text", "supervisory_guidance", "industry_position",
        "expert_opinion", "consulting_framework", "research_report",
        "vendor_marketing", "blog_article", "press_article",
        "internal_strategy", "unknown"
    ],
    "origin": [
        "supervisory_authority", "legislator", "industry_association",
        "consulting_firm", "research_institution", "cloud_vendor",
        "software_vendor", "corporate", "media", "internal", "unknown"
    ]
}

ORIGIN_SHORT = {
    "legislator":            "eu",
    "supervisory_authority": "supervisory",
    "consulting_firm":       "consulting",
    "cloud_vendor":          "aws",
    "software_vendor":       "vendor",
    "industry_association":  "industry",
    "research_institution":  "research",
    "corporate":             "corporate",
    "media":                 "media",
    "internal":              "internal",
    "unknown":               "unknown",
}


def _validate_patch(patch: Dict) -> None:
    doc_id = patch.get("doc_id")
    fields = patch.get("fields", {})

    if not doc_id:
        raise ValueError("Patch missing 'doc_id'")
    if not fields:
        raise ValueError(f"Patch for '{doc_id}' has no 'fields'")

    for field, value in fields.items():
        if field not in VALID_FIELDS:
            raise ValueError(
                f"Field '{field}' not supported. "
                f"Allowed: {sorted(VALID_FIELDS)}"
            )
        if value not in VALID_VALUES[field]:
            raise ValueError(
                f"Value '{value}' not valid for '{field}'. "
                f"Allowed: {VALID_VALUES[field]}"
            )


# ============================================================
# REGISTRY
# ============================================================

def _load_registry() -> List[Dict]:
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Registry not found: {REGISTRY_PATH}")
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_registry(registry: List[Dict]) -> None:
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)


def _find_registry_entry(registry: List[Dict], doc_id: str) -> Optional[Dict]:
    for entry in registry:
        if entry.get("doc_id") == doc_id:
            return entry
    return None


# ============================================================
# DOC-ID GENERATION (inline — kein Import-Overhead)
# ============================================================

def _rebuild_doc_id(old_doc_id: str, new_origin: str) -> str:
    """
    Generiert neue doc_id bei Origin-Änderung.
    Strategie: altes doc_id-Schema ist doc_{origin_short}_{rest}
    Ersetze nur das origin_short-Präfix.

    Beispiel:
      old: doc_research_digitales_2025_913b5f
      new origin: industry_association → short: industry
      new: doc_industry_digitales_2025_913b5f
    """
    # Altes origin_short aus doc_id extrahieren
    # Schema: doc_{origin_short}_{...rest}
    parts = old_doc_id.split("_", 2)  # ["doc", origin_short, "rest..."]
    if len(parts) < 3:
        raise ValueError(f"Cannot parse doc_id: '{old_doc_id}'")

    new_short = ORIGIN_SHORT.get(new_origin, "unknown")
    new_doc_id = f"doc_{new_short}_{parts[2]}"

    return new_doc_id


# ============================================================
# CHUNKS
# ============================================================

def _load_chunks() -> List[Dict]:
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(f"chunks.json not found: {CHUNKS_PATH}")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_chunks(chunks: List[Dict]) -> None:
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)


def _rename_chunks(chunks: List[Dict], old_doc_id: str, new_doc_id: str) -> Tuple[List[Dict], int]:
    """
    Benennt doc_id und chunk_id in chunks.json um.
    chunk_id-Schema: {doc_id}_chunk_{n}
    """
    count = 0
    for chunk in chunks:
        if chunk.get("doc_id") == old_doc_id:
            old_chunk_id = chunk["chunk_id"]
            # chunk_id = old_doc_id + "_chunk_NNN"
            suffix = old_chunk_id[len(old_doc_id):]  # z.B. "_chunk_000"
            chunk["chunk_id"] = new_doc_id + suffix
            chunk["doc_id"] = new_doc_id
            count += 1
    return chunks, count


# ============================================================
# VECTOR INDEX
# ============================================================

def _load_chunk_ids() -> List[str]:
    if not CHUNK_IDS_PATH.exists():
        raise FileNotFoundError(f"chunk_ids.json not found: {CHUNK_IDS_PATH}")
    with open(CHUNK_IDS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_embeddings() -> np.ndarray:
    if not EMBEDDINGS_PATH.exists():
        raise FileNotFoundError(f"embeddings.pt not found: {EMBEDDINGS_PATH}")
    return torch.load(EMBEDDINGS_PATH).numpy()


def _rebuild_vector_index(old_doc_id: str, new_doc_id: str) -> int:
    """
    Umbenennung der Chunk-IDs im Vector Index bei doc_id-Änderung.

    KEIN Re-Encoding — Vektoren bleiben identisch.
    Nur Positions-Mapping wird neu sortiert.

    Reihenfolge-Invariante (IndexConsistencyCheck):
      chunk_ids.json muss sortiert sein.
      embeddings.pt[i] entspricht sorted(chunk_ids)[i].
      FAISS-Index ist aligned mit embeddings.pt.

    Vorgehen:
      1. Baue mapping: chunk_id → embedding-vector (current sorted positions)
      2. Benenne betroffene chunk_ids um (prefix-replace)
      3. Sortiere neu → neue Positionen
      4. Reorder embeddings entsprechend neuer Reihenfolge
      5. Rebuild FAISS (reine Neuindexierung, keine neuen Vektoren)
      6. Speichere alle Artefakte atomisch
    """
    chunk_ids = _load_chunk_ids()   # sorted list
    embeddings = _load_embeddings() # aligned with chunk_ids

    if len(chunk_ids) != len(embeddings):
        raise ValueError(
            f"Alignment broken: {len(chunk_ids)} chunk_ids vs "
            f"{len(embeddings)} embeddings"
        )

    # 1. Build id → vector mapping
    id_to_vector: Dict[str, np.ndarray] = {
        cid: embeddings[i]
        for i, cid in enumerate(chunk_ids)
    }

    # 2. Rename affected chunk_ids
    renamed_count = 0
    old_prefix = old_doc_id + "_chunk_"
    new_prefix = new_doc_id + "_chunk_"

    new_id_to_vector: Dict[str, np.ndarray] = {}
    for cid, vec in id_to_vector.items():
        if cid.startswith(old_prefix):
            new_cid = new_prefix + cid[len(old_prefix):]
            new_id_to_vector[new_cid] = vec
            renamed_count += 1
        else:
            new_id_to_vector[cid] = vec

    # 3. Sort → new canonical order
    sorted_ids = sorted(new_id_to_vector.keys())

    # 4. Reorder embeddings
    reordered = np.array([new_id_to_vector[cid] for cid in sorted_ids])

    # 5. Rebuild FAISS
    dim = reordered.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(reordered.astype("float32"))

    # 6. Persist (atomic sequence)
    torch.save(torch.tensor(reordered), EMBEDDINGS_PATH)
    faiss.write_index(index, str(FAISS_INDEX_PATH))
    with open(CHUNK_IDS_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted_ids, f, indent=2)

    return renamed_count


# ============================================================
# AUDIT LOG
# ============================================================

def _write_audit(doc_id: str, new_doc_id: Optional[str], fields: Dict, dry_run: bool) -> None:
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": "reclassify",
        "doc_id": doc_id,
        "new_doc_id": new_doc_id,
        "fields": fields,
        "dry_run": dry_run
    }
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


# ============================================================
# CONSISTENCY CHECK (inline runner)
# ============================================================

def _run_consistency_check() -> None:
    from knowledge_construction.embedding.index_consistency_check import IndexConsistencyCheck
    IndexConsistencyCheck().run()


# ============================================================
# CORE: APPLY PATCH
# ============================================================

def _apply_patch(patch: Dict, registry: List[Dict], dry_run: bool) -> Optional[str]:
    """
    Wendet einen einzelnen Patch an.
    Gibt die neue doc_id zurück (oder None wenn doc_id unverändert).
    """

    doc_id = patch["doc_id"]
    fields = patch["fields"]

    entry = _find_registry_entry(registry, doc_id)
    if entry is None:
        print(f"  ⚠  doc_id nicht gefunden: {doc_id} — übersprungen")
        return None

    print(f"\n  Dokument : {doc_id}")
    print(f"  Titel    : {entry.get('title', '—')}")

    new_doc_id: Optional[str] = None

    # -------------------------------------------------------
    # CASE A: document_type change — Registry only
    # -------------------------------------------------------

    if "document_type" in fields and "origin" not in fields:
        old_val = entry.get("document_type")
        new_val = fields["document_type"]
        print(f"  document_type: {old_val}  →  {new_val}")

        if not dry_run:
            entry["document_type"] = new_val

    # -------------------------------------------------------
    # CASE B: origin change — Registry + Chunks + Vector Index
    # -------------------------------------------------------

    if "origin" in fields:
        old_origin = entry.get("origin")
        new_origin = fields["origin"]
        new_doc_id = _rebuild_doc_id(doc_id, new_origin)

        print(f"  origin   : {old_origin}  →  {new_origin}")
        print(f"  doc_id   : {doc_id}  →  {new_doc_id}")

        # Prüfen ob neue doc_id bereits existiert
        conflict = _find_registry_entry(registry, new_doc_id)
        if conflict:
            raise ValueError(
                f"Konflikt: neue doc_id '{new_doc_id}' existiert bereits in der Registry"
            )

        if not dry_run:
            entry["origin"] = new_origin
            entry["doc_id"] = new_doc_id

            # Chunks umbenennen
            chunks = _load_chunks()
            chunks, chunk_count = _rename_chunks(chunks, doc_id, new_doc_id)
            _save_chunks(chunks)
            print(f"  Chunks umbenannt : {chunk_count}")

            # Vector Index reorder
            renamed_in_index = _rebuild_vector_index(doc_id, new_doc_id)
            print(f"  Vector Index aktualisiert : {renamed_in_index} Einträge")

    return new_doc_id


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="TD-007: Reklassifizierungs-Skript für die Strategic Knowledge Engine"
    )
    parser.add_argument(
        "--patch",
        required=True,
        help="Pfad zur Patch-Datei (JSON)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Zeigt geplante Änderungen ohne Dateien zu schreiben"
    )
    args = parser.parse_args()

    patch_path = Path(args.patch)
    if not patch_path.exists():
        print(f"❌ Patch-Datei nicht gefunden: {patch_path}")
        sys.exit(1)

    with open(patch_path, "r", encoding="utf-8") as f:
        patches = json.load(f)

    if not isinstance(patches, list):
        print("❌ Patch-Datei muss ein JSON-Array sein")
        sys.exit(1)

    if args.dry_run:
        print("\n⚡ DRY-RUN — keine Dateien werden geschrieben\n")
    else:
        print("\n🔧 Reklassifizierung startet\n")

    # Validation
    print("Validierung...")
    for patch in patches:
        try:
            _validate_patch(patch)
        except ValueError as e:
            print(f"❌ Validierungsfehler: {e}")
            sys.exit(1)
    print(f"✔ {len(patches)} Patch(es) validiert\n")

    # Load Registry once
    registry = _load_registry()
    print(f"Registry geladen: {len(registry)} Dokumente\n")
    print("-" * 60)

    applied = 0
    errors = 0

    for patch in patches:
        try:
            new_doc_id = _apply_patch(patch, registry, args.dry_run)
            if not args.dry_run:
                _write_audit(
                    doc_id=patch["doc_id"],
                    new_doc_id=new_doc_id,
                    fields=patch["fields"],
                    dry_run=args.dry_run
                )
            applied += 1
        except Exception as e:
            print(f"  ❌ Fehler: {e}")
            errors += 1

    print("\n" + "-" * 60)

    if not args.dry_run and applied > 0:
        # Registry speichern (einmalig am Ende — alle Änderungen in-memory)
        _save_registry(registry)
        print(f"\n✔ Registry gespeichert ({applied} Patch(es) angewendet)")

        # Consistency Check
        print("\nKonsistenz-Prüfung...")
        try:
            _run_consistency_check()
        except Exception as e:
            print(f"❌ Konsistenz-Prüfung fehlgeschlagen: {e}")
            sys.exit(1)
    else:
        print(f"\n✔ Dry-run abgeschlossen — {applied} Änderung(en) simuliert")

    if errors > 0:
        print(f"\n⚠  {errors} Patch(es) fehlgeschlagen")
        sys.exit(1)