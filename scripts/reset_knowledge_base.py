import shutil
from pathlib import Path
from datetime import datetime

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path(__file__).resolve().parent.parent

ARCHIVE_PATH = BASE_PATH / "knowledge_sources" / "archive"
INTAKE_PATH = BASE_PATH / "knowledge_sources" / "intake"
KB_PATH = BASE_PATH / "knowledge_base"

BACKUP_ENABLED = True


# --------------------------------------------------
# UTILS
# --------------------------------------------------

def ensure_directory(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def clear_directory(path: Path):
    if not path.exists():
        return
    for item in path.iterdir():
        if item.is_file():
            item.unlink()
        else:
            shutil.rmtree(item)


def backup_directory(path: Path):
    if not path.exists():
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = path.parent / "99_Backup" / f"{path.name}_backup_{timestamp}"

    print(f"📦 Creating backup: {backup_path}")
    shutil.copytree(path, backup_path)

    return backup_path


# --------------------------------------------------
# STEP 1 – MOVE ARCHIVE → INTAKE
# --------------------------------------------------

def restore_documents_to_intake():
    """
    Moves documents from archive/ back to intake/ for re-onboarding.
    
    This prepares the system for a full re-processing cycle.
    After this, intake/ contains all previously processed documents,
    ready to be re-onboarded with potentially updated classifiers/governance rules.
    """
    
    if not ARCHIVE_PATH.exists():
        print("⚠ Archive directory not found — nothing to restore")
        return 0

    print("\n🔁 Moving documents from archive → intake (for re-onboarding)")
    
    ensure_directory(INTAKE_PATH)
    
    count = 0
    
    for file in ARCHIVE_PATH.rglob("*"):
        if file.is_file():
            # Preserve directory structure relative to archive
            relative_path = file.relative_to(ARCHIVE_PATH)
            target_path = INTAKE_PATH / relative_path
            
            # Create parent directories if needed
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file (not copy)
            shutil.move(str(file), str(target_path))
            count += 1
    
    print(f"✅ {count} document(s) moved to intake")
    return count


# --------------------------------------------------
# STEP 2 – RESET KNOWLEDGE BASE
# --------------------------------------------------

def reset_knowledge_base():
    """
    Clears all knowledge base artifacts:
    - registry (document_registry.json)
    - chunks (chunks.json)
    - vector_index (FAISS index, embeddings, chunk_ids)
    - audit logs
    
    After this, the knowledge base is empty and ready for fresh onboarding.
    """
    
    print("\n🧹 Resetting Knowledge Base")

    if BACKUP_ENABLED:
        backup_directory(KB_PATH)

    subpaths = [
        KB_PATH / "registry",
        KB_PATH / "chunks",
        KB_PATH / "vector_index",
        KB_PATH / "audit"
    ]

    for path in subpaths:
        print(f" - clearing {path}")
        clear_directory(path)
        ensure_directory(path)

    print("✅ Knowledge Base reset complete")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("\n" + "=" * 60)
    print("🚀 RESET KNOWLEDGE BASE & PREPARE FOR RE-ONBOARDING")
    print("=" * 60)
    
    # Step 1: Move archive → intake
    doc_count = restore_documents_to_intake()
    
    # Step 2: Reset knowledge base
    reset_knowledge_base()
    
    print("\n" + "=" * 60)
    print("✅ RESET COMPLETE")
    print("=" * 60)
    print(f"\nState after reset:")
    print(f"  intake/:     {doc_count} documents (ready for re-onboarding)")
    print(f"  archive/:    empty")
    print(f"  knowledge_base/: empty")
    print(f"\nNext step:")
    print(f"  python -m scripts.run_onboarding")
    print()


if __name__ == "__main__":
    main()