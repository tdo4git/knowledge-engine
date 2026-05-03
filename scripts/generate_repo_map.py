from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "node_modules",
    "vector_index",
    "chunks",
    ".gitignore",
    ".DS_Store"
}

MAX_DEPTH = 4


def build_tree(path, prefix="", depth=0):
    if depth > MAX_DEPTH:
        return ""

    lines = []
    entries = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))

    for i, entry in enumerate(entries):
        if entry.name in EXCLUDE_DIRS:
            continue

        connector = "└── " if i == len(entries) - 1 else "├── "
        lines.append(f"{prefix}{connector}{entry.name}")

        if entry.is_dir():
            extension = "    " if i == len(entries) - 1 else "│   "
            lines.append(build_tree(entry, prefix + extension, depth + 1))

    return "\n".join([l for l in lines if l])


def main():
    print("knowledge-engine/")
    print(build_tree(BASE_PATH))


if __name__ == "__main__":
    main()