
import os
from agent.ollama_provider import OllamaAIProvider
from agent.hosted_provider import HostedAIProvider
from agent.ai_config import get_ai_config
from agent.ai_provider import MockAIProvider
from agent.nebius_provider import NebiusAIProvider


def create_ai_provider():
    """
    Select an AI provider based on environment configuration.

    Mock is the default provider.
    Nebius requires an API key.
    Ollama will be connected in a later step.
    """

    config = get_ai_config()
    provider = config["provider"]

    if provider == "mock":
        return MockAIProvider()

    if provider == "nebius":
        if not config["configured"]:
            raise ValueError(
                "Nebius is selected but no API key is configured."
            )

        return NebiusAIProvider(
            api_key=os.environ["NEBIUS_API_KEY"]
        )

    if provider == "ollama":
      return OllamaAIProvider()

    if provider == "hosted":
      return HostedAIProvider()

    raise ValueError(
        f"Unsupported AI provider: {provider}"
    )
