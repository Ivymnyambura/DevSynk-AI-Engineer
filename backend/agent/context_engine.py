from agent.secret_scanner import scan_code_for_secrets
from agent.repository import read_repository_file
from agent.repository_intelligence import analyze_repository
from agent.dependency_analyzer import (
    find_dependent_files,
    find_all_dependent_files,
)


def build_file_context(
    file_path: str,
    repository_path: str = "."
) -> dict:
    """
    Build structured context for a repository file.
    No AI calls or code execution.
    """

    repository = analyze_repository(repository_path)

    analyzed_files = repository["files"]

    file_analysis = next(
        (
            item for item in analyzed_files
            if item["file"] == file_path
        ),
        None
    )

    if file_analysis is None:
        raise ValueError(
            "File not found in analyzed repository"
        )

    code = read_repository_file(
        repository_path,
        file_path
    )

    
    secret_scan = scan_code_for_secrets(code)

    if secret_scan["secrets_detected"]:
        raise ValueError(
            "File contains potentially sensitive credentials "
            "and cannot be included in AI context."
        )


    direct_dependents = find_dependent_files(
        file_path,
        analyzed_files
    )

    all_dependents = find_all_dependent_files(
        file_path,
        analyzed_files
    )

    return {
        "file": file_path,
        "code": code,
        "inspection": file_analysis["inspection"],
        "dependencies": file_analysis["dependencies"],
        "resolved_dependencies": file_analysis[
            "resolved_dependencies"
        ],
        "direct_dependents": direct_dependents,
        "indirect_dependents": [
            item for item in all_dependents
            if item not in direct_dependents
        ]
    }



def build_related_context(
    file_path: str,
    repository_path: str = ".",
    max_files: int = 5,
    max_characters: int = 30000
) -> dict:
    """
    Collect a primary file and its direct local dependencies,
    subject to file count and source code size limits.
    """

    if not 1 <= max_files <= 10:
        raise ValueError("max_files must be between 1 and 10")

    if not 1 <= max_characters <= 100000:
        raise ValueError(
            "max_characters must be between 1 and 100000"
        )

    primary = build_file_context(
        file_path,
        repository_path
    )

    primary_size = len(primary["code"])

    if primary_size > max_characters:
        raise ValueError(
            "Primary file exceeds the context size limit"
        )

    related_files = []
    seen = {file_path}
    total_characters = primary_size
    omitted_files = []

    for dependency in primary["resolved_dependencies"]:
        dependency_path = dependency["file"]

        if dependency_path in seen:
            continue

        seen.add(dependency_path)

        if len(related_files) + 1 >= max_files:
            omitted_files.append(dependency_path)
            continue

        related = build_file_context(
            dependency_path,
            repository_path
        )

        related_size = len(related["code"])

        if total_characters + related_size > max_characters:
            omitted_files.append(dependency_path)
            continue

        related_files.append(related)
        total_characters += related_size

    return {
        "primary_file": file_path,
        "total_context_files": 1 + len(related_files),
        "total_code_characters": total_characters,
        "omitted_files": omitted_files,
        "files": [primary, *related_files]
    }
