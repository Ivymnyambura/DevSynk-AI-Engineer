
from pathlib import Path

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "dist",
    "build",
    ".angular"
}


IGNORED_FILES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    "credentials.json",
    "secrets.json",
    "id_rsa",
    "id_ed25519",
}

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx",
    ".java", ".json", ".html", ".css",
    ".md", ".txt", ".yml", ".yaml"
}



SENSITIVE_FILENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "credentials.json",
    "secrets.json",
    "service-account.json",
    "id_rsa",
    "id_ed25519"
}

SENSITIVE_EXTENSIONS = {
    ".pem",
    ".key",
    ".p12",
    ".pfx"
}


def list_repository_files(repository_path: str) -> list[str]:
    """
    Return a list of files in a local repository.
    Ignore generated files and dependency folders.
    """

    root = Path(repository_path).resolve()

    if not root.is_dir():
        raise ValueError("Repository directory does not exist.")

    files = []

    for current_root, directories, filenames in __import__("os").walk(root):
        directories[:] = [
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES
        ]

        for filename in filenames:
            file_path = Path(current_root) / filename
            relative_path = file_path.relative_to(root)
            files.append(relative_path.as_posix())

    return sorted(files)



def read_repository_file(
    repository_path: str,
    file_path: str
) -> str:
    """
    Read a permitted source file from a local repository.
    """

    root = Path(repository_path).resolve()

    if not root.is_dir():
        raise ValueError("Repository directory does not exist.")

    requested_file = Path(file_path)

    if requested_file.is_absolute():
        raise ValueError("Absolute file paths are not allowed.")

    # Reject parent-directory traversal and ignored paths.
    if ".." in requested_file.parts:
        raise ValueError("Access outside repository is not allowed.")

    if any(
        part in IGNORED_DIRECTORIES
        for part in requested_file.parts
    ):
        raise ValueError("Access to ignored directories is not allowed.")

    if requested_file.name.lower() in IGNORED_FILES:
        raise ValueError("Sensitive files cannot be accessed.")

    if requested_file.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type.")

    # Reject symbolic links at every path component.
    current = root

    for part in requested_file.parts:
        current = current / part

        if current.is_symlink():
            raise ValueError("Symbolic links are not allowed.")

    target = current.resolve()

    if not target.is_relative_to(root):
        raise ValueError("Access outside repository is not allowed.")

    if not target.is_file():
        raise ValueError("Requested file does not exist.")

    if target.stat().st_size > 100_000:
        raise ValueError("File exceeds the maximum allowed size.")

    return target.read_text(encoding="utf-8")
