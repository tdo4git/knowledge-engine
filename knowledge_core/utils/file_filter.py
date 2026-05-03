import os
from config.file_config import ALLOWED_EXTENSIONS, IGNORE_HIDDEN_FILES


def is_valid_file(filename: str) -> bool:
    """
    Prüft, ob eine Datei für das Onboarding zugelassen ist.
    """

    # Hidden files (z. B. .DS_Store)
    if IGNORE_HIDDEN_FILES and filename.startswith("."):
        return False

    # Extension check
    _, ext = os.path.splitext(filename.lower())

    if ext not in ALLOWED_EXTENSIONS:
        return False

    return True