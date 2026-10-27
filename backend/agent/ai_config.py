
import os


SUPPORTED_AI_PROVIDERS = {
    "mock",
    "hosted",
    "ollama",
    "nebius"
}


def get_ai_config() -> dict:
    """
    Return the current DevSynk AI provider configuration.

    Hosted AI is the intended production default.
    Mock remains the development default until hosted
    inference is implemented and configured.
    """

    provider = os.getenv(
        "DEVSYNK_AI_PROVIDER",
        "mock"
    ).strip().lower()

    if provider not in SUPPORTED_AI_PROVIDERS:
        raise ValueError(
            f"Unsupported AI provider: {provider}"
        )

    
    nebius_api_key = os.getenv(
        "NEBIUS_API_KEY", ""
    ).strip()

    hosted_api_url = os.getenv(
        "DEVSYNK_HOSTED_AI_URL", ""
    ).strip()

    hosted_model = os.getenv(
        "DEVSYNK_HOSTED_AI_MODEL", ""
    ).strip()

    hosted_api_key = os.getenv(
        "DEVSYNK_HOSTED_AI_API_KEY", ""
    ).strip()


    if provider == "mock":
        configured = True

    elif provider == "ollama":
        configured = True

    elif provider == "nebius":
        configured = bool(nebius_api_key.strip())

    
    else:
        configured = all([
            hosted_api_url,
            hosted_model,
            hosted_api_key
        ])


    return {
        "provider": provider,
        "configured": configured,
        "api_key_present": (
            bool(nebius_api_key.strip())
            if provider == "nebius"
            else False
        ),
        "hosted_endpoint_present": (
            bool(hosted_api_url.strip())
            if provider == "hosted"
            else False
        ),
        "supported_providers": sorted(
            SUPPORTED_AI_PROVIDERS
        )
    }
