
from pathlib import Path


LANGUAGE_EXTENSIONS = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".java": "java",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",
    ".json": "json",
    ".sql": "sql",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".md": "markdown",
    ".sh": "shell",
    ".ps1": "powershell",
}


def detect_language(file_path: str) -> str:
    """
    Detect a source file's language using its extension.
    """

    extension = Path(file_path).suffix.lower()

    return LANGUAGE_EXTENSIONS.get(
        extension,
        "unknown"
    )
