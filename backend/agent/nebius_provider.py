
from agent.ai_provider import AIProvider


class NebiusAIProvider(AIProvider):
    """
    Adapter for Nebius Token Factory.

    Network requests are not implemented yet.
    """

    def __init__(self, api_key: str):
        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError(
                "Nebius API key is required."
            )

        self._api_key = api_key

    def analyze_code(self, issue: str, code: str) -> dict:
        raise NotImplementedError(
            "Nebius code analysis is not implemented yet."
        )

    def answer_question(
        self,
        question: str,
        context: dict
    ) -> dict:
        raise NotImplementedError(
            "Nebius question answering is not implemented yet."
        )
