
import re


SECRET_PATTERNS = {
    "private_key": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
    "github_token": re.compile(
        r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b"
    ),
    "aws_access_key": re.compile(
        r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"
    ),
    "generic_credential": re.compile(
        r"""(?i)\b(?:api_key|secret_key|access_token|
        client_secret|password)\b\s*[:=]\s*["'][^"'\r\n]{8,}["']""",
        re.VERBOSE
    )
}


def scan_code_for_secrets(code: str) -> dict:
    """
    Detect common credential patterns without returning
    the potentially sensitive values.
    """

    findings = []

    for name, pattern in SECRET_PATTERNS.items():
        for match in pattern.finditer(code):
            line_number = code.count(
                "\n", 0, match.start()
            ) + 1

            findings.append({
                "type": name,
                "line": line_number
            })

    return {
        "secrets_detected": bool(findings),
        "findings": findings
    }
