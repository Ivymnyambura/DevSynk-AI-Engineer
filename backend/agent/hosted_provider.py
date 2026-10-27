
import os

from agent.ai_provider import AIProvider


class HostedAIProvider(AIProvider):
    """
    Adapter for DevSynk's future hosted AI service.

    Hosted inference is not implemented yet.
    """

    
    def __init__(self):
        self.endpoint = os.getenv(
            "DEVSYNK_HOSTED_AI_URL", ""
        ).strip()

        self.model = os.getenv(
            "DEVSYNK_HOSTED_AI_MODEL", ""
        ).strip()

        self.api_key = os.getenv(
            "DEVSYNK_HOSTED_AI_API_KEY", ""
        ).strip()

        if not self.endpoint:
            raise ValueError(
                "Hosted AI is not configured. "
                "Set DEVSYNK_HOSTED_AI_URL."
            )

        if not self.endpoint.startswith(
            ("https://", "http://")
        ):
            raise ValueError(
                "Hosted AI endpoint must be an HTTP or HTTPS URL."
            )

        if not self.model:
            raise ValueError(
                "Hosted AI model is not configured. "
                "Set DEVSYNK_HOSTED_AI_MODEL."
            )

        if not self.api_key:
            raise ValueError(
                "Hosted AI API key is not configured. "
                "Set DEVSYNK_HOSTED_AI_API_KEY."
            )

    def analyze_code(self, issue: str, code: str) -> dict:
        raise NotImplementedError(
            "Hosted AI code analysis is not implemented yet."
        )

    def answer_question(self, question: str, context: dict) -> dict:
        raise NotImplementedError(
            "Hosted AI question answering is not implemented yet."
        )
