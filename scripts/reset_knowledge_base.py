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
# STEP 0 – CLEAN INTAKE
# --------------------------------------------------

#def reset_intake():
#    print("\n🧹 Clearing intake directory")
#    ensure_directory(INTAKE_PATH)
#    clear_directory(INTAKE_PATH)
#    print("✅ Intake cleared")


# --------------------------------------------------
# STEP 1 – COPY ARCHIVE → INTAKE
# --------------------------------------------------

def copy_archive_to_intake():
    print("\n🔁 Copying documents from archive → intake")

    count = 0

    for file in ARCHIVE_PATH.rglob("*"):
        if file.is_file():
            relative_path = file.relative_to(ARCHIVE_PATH)
            target_path = INTAKE_PATH / relative_path

            ensure_directory(target_path.parent)
            shutil.copy2(file, target_path)

            count += 1

    print(f"✅ {count} documents copied to intake")


# --------------------------------------------------
# STEP 2 – RESET KNOWLEDGE BASE
# --------------------------------------------------

def reset_knowledge_base():
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
    print("🚀 Knowledge Base Reset & Re-Onboarding Preparation")

    if not ARCHIVE_PATH.exists():
        raise ValueError(f"Archive path not found: {ARCHIVE_PATH}")

    # Step 0
    #reset_intake()

    # Step 1
    copy_archive_to_intake()

    # Step 2
    reset_knowledge_base()

    print("\n🎯 System ready for full re-onboarding")


if __name__ == "__main__":
    main()