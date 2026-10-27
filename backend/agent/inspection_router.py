import json
import subprocess
from pathlib import Path
from agent.language_detector import detect_language
from agent.code_inspector import inspect_python_code


TOOLS_DIRECTORY = Path(__file__).resolve().parent.parent / "tools"
TYPESCRIPT_INSPECTOR = TOOLS_DIRECTORY / "typescript_inspector.cjs"


def inspect_typescript_code(file_path: str, code: str) -> dict:
    """
    Inspect TypeScript or JavaScript without executing
    the source code being analyzed.
    """

    payload = json.dumps({
        "file_path": file_path,
        "code": code
    })

    try:
        result = subprocess.run(
            ["node", str(TYPESCRIPT_INSPECTOR)],
            input=payload,
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )

    except (OSError, subprocess.TimeoutExpired) as error:
        return {
            "language": detect_language(file_path),
            "status": "inspection_failed",
            "error": str(error)
        }

    if result.returncode != 0:
        return {
            "language": detect_language(file_path),
            "status": "inspection_failed",
            "error": result.stderr.strip()
        }

    try:
        return json.loads(result.stdout)

    except json.JSONDecodeError:
        return {
            "language": detect_language(file_path),
            "status": "inspection_failed",
            "error": "Inspector returned invalid JSON."
        }



def inspect_code(file_path: str, code: str) -> dict:
    """
    Route source code to the appropriate language inspector.
    """

    language = detect_language(file_path)

    if language == "python":
        return inspect_python_code(code)

        
    if language in {"typescript", "javascript"}:
        return inspect_typescript_code(file_path, code)

    if language == "json":
        return inspect_json_code(code)

    return {
        "language": language,
        "syntax_valid": None,
        "functions": [],
        "classes": [],
        "errors": [],
        "status": "inspector_not_implemented"
    }


def inspect_json_code(code: str) -> dict:
    """
    Validate JSON syntax without executing code.
    """

    try:
        json.loads(code)

        return {
            "language": "json",
            "syntax_valid": True,
            "functions": [],
            "classes": [],
            "errors": []
        }

    except json.JSONDecodeError as error:
        return {
            "language": "json",
            "syntax_valid": False,
            "functions": [],
            "classes": [],
            "errors": [
                {
                    "line": error.lineno,
                    "message": error.msg
                }
            ]
        }
