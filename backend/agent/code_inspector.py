
import ast


def inspect_python_code(code: str) -> dict:
    """
    Check Python source code for syntax errors
    without executing it.
    """

    try:
        tree = ast.parse(code)

        functions = [
            node.name
            for node in ast.walk(tree)
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            )
        ]

        classes = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        ]

        return {
            "language": "python",
            "syntax_valid": True,
            "functions": functions,
            "classes": classes,
            "errors": []
        }

    except SyntaxError as error:
        return {
            "language": "python",
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
