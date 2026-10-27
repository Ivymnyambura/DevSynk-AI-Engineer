
from pathlib import Path

from agent.dependency_analyzer import (
    analyze_python_dependencies,
    resolve_python_dependencies,
    resolve_typescript_dependencies,
)
from agent.repository import (
    list_repository_files,
    read_repository_file,
)
from agent.inspection_router import inspect_code


def analyze_repository(repository_path: str = ".") -> dict:
    """
    Analyze supported source files in a repository
    without executing their contents.

    Inspect syntax, discover imports, and resolve
    supported local dependencies.
    """

    files = list_repository_files(repository_path)

    source_files = [
        file for file in files
        if Path(file).suffix.lower() in {
            ".py", ".ts", ".tsx", ".js", ".jsx",
            ".java", ".html", ".css", ".scss",
            ".json", ".sql", ".yml", ".yaml"
        }
    ]

    results = []
    skipped_files = []

    for file in source_files:
        try:
            code = read_repository_file(
                repository_path,
                file
            )

            inspection = inspect_code(file, code)

            dependencies = (
                analyze_python_dependencies(code)
                if file.endswith(".py")
                else None
            )

            if (
                file.endswith(".py")
                and dependencies
                and dependencies["syntax_valid"]
            ):
                resolved_dependencies = resolve_python_dependencies(
                    dependencies["imports"],
                    files
                )

            elif (
                Path(file).suffix.lower()
                in {".ts", ".tsx", ".js", ".jsx"}
            ):
                resolved_dependencies = (
                    resolve_typescript_dependencies(
                        file,
                        inspection.get("imports", []),
                        files
                    )
                    if inspection.get("syntax_valid")
                    else []
                )

            else:
                resolved_dependencies = []

            results.append({
                "file": file,
                "inspection": inspection,
                "dependencies": dependencies,
                "resolved_dependencies": resolved_dependencies
            })

        except (ValueError, UnicodeError, OSError) as error:
            skipped_files.append({
                "file": file,
                "reason": str(error)
            })

    return {
        "total_repository_files": len(files),
        "source_files_found": len(source_files),
        "source_files_processed": len(results),
        "files": results,
        "skipped_files": skipped_files
    }
