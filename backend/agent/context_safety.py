
from agent.secret_scanner import scan_code_for_secrets


def validate_ai_context(context: dict) -> dict:
    """
    Validate source-code context before it is
    passed to an AI provider.

    Rejects missing, malformed, or sensitive context.
    """

    if not isinstance(context, dict):
        raise ValueError("AI context must be an object.")

    files = context.get("files")

    if not isinstance(files, list) or not files:
        raise ValueError("AI context must contain files.")

    for file in files:
        if not isinstance(file, dict):
            raise ValueError("Invalid file context.")

        code = file.get("code")

        if not isinstance(code, str):
            raise ValueError("File context must contain source code.")

        scan = scan_code_for_secrets(code)

        if scan["secrets_detected"]:
            raise ValueError(
                "AI context contains potentially sensitive "
                "credentials and cannot be sent to a provider."
            )

    return context
