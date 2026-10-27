
import ast
from pathlib import PurePosixPath

def analyze_python_dependencies(code: str) -> dict:
    """
    Discover Python imports without executing source code.
    """

    try:
        tree = ast.parse(code)

    except SyntaxError as error:
        return {
            "language": "python",
            "imports": [],
            "syntax_valid": False,
            "errors": [
                {
                    "line": error.lineno,
                    "message": error.msg
                }
            ]
        }

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    "module": alias.name,
                    "type": "import"
                })

        elif isinstance(node, ast.ImportFrom):
            imports.append({
                "module": "." * node.level + (node.module or ""),
                "type": "from_import",
                "names": [
                    alias.name for alias in node.names
                ]
            })

    return {
        "language": "python",
        "imports": imports,
        "syntax_valid": True,
        "errors": []
    }


def resolve_python_dependencies(
    imports: list,
    repository_files: list
) -> list:
    """
    Match absolute Python module imports to repository files.
    """

    available_files = set(repository_files)
    resolved = []

    for item in imports:
        module = item.get("module", "")

        # Relative imports need separate resolution logic.
        if not module or module.startswith("."):
            continue

        module_path = module.replace(".", "/")

        candidates = [
            f"{module_path}.py",
            f"{module_path}/__init__.py"
        ]

        for candidate in candidates:
            if candidate in available_files:
                resolved.append({
                    "module": module,
                    "file": candidate
                })
                break

    return resolved


def find_dependent_files(
    target_file: str,
    analyzed_files: list
) -> list:
    """
    Find repository files that directly import the target file.
    """

    dependents = []

    for item in analyzed_files:
        for dependency in item.get("resolved_dependencies", []):
            if dependency["file"] == target_file:
                dependents.append(item["file"])
                break

    return dependents


def find_all_dependent_files(
    target_file: str,
    analyzed_files: list
) -> list:
    """
    Find files that directly or indirectly depend on a target.
    """

    visited = {target_file}
    pending = [target_file]
    dependents = []

    while pending:
        current_file = pending.pop(0)

        direct_dependents = find_dependent_files(
            current_file,
            analyzed_files
        )

        for dependent in direct_dependents:
            if dependent not in visited:
                visited.add(dependent)
                dependents.append(dependent)
                pending.append(dependent)

    return dependents


def resolve_typescript_dependencies(
    source_file: str,
    imports: list,
    repository_files: list
) -> list:
    """
    Resolve relative TypeScript and JavaScript imports
    to existing repository files.
    """

    available_files = set(repository_files)
    resolved = []

    for item in imports:
        module = item.get("module", "")

        if not module.startswith("."):
            continue

        source_parts = list(PurePosixPath(source_file).parent.parts)

        if source_parts == ["."]:
            source_parts = []

        for part in module.split("/"):
            if part in ("", "."):
                continue

            if part == "..":
                if not source_parts:
                    break
                source_parts.pop()
            else:
                source_parts.append(part)
        else:
            base_path = "/".join(source_parts)

            candidates = [
                base_path + extension
                for extension in (".ts", ".tsx", ".js", ".jsx")
            ] + [
                base_path + "/index" + extension
                for extension in (".ts", ".tsx", ".js", ".jsx")
            ]

            for candidate in candidates:
                if candidate in available_files:
                    resolved.append({
                        "module": module,
                        "file": candidate
                    })
                    break

    return resolved
