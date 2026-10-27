
import os
import json
from urllib import request, error


def check_ollama_health() -> dict:
    """
    Check whether the local Ollama service is reachable
    and whether the selected AI model is installed.
    """

    url = "http://127.0.0.1:11434/api/tags"

    selected_model = os.getenv(
        "OLLAMA_MODEL",
        "qwen2.5-coder:0.5b"
    )

    try:
        with request.urlopen(url, timeout=3) as response:
            data = json.load(response)

        models = data.get("models", [])

        if not isinstance(models, list):
            raise ValueError("Invalid Ollama model list.")

        model_names = [
            model["name"]
            for model in models
            if isinstance(model, dict)
            and isinstance(model.get("name"), str)
        ]

        model_ready = selected_model in model_names

        return {
            "provider": "ollama",
            "available": True,
            "models": model_names,
            "model_count": len(model_names),
            "selected_model": selected_model,
            "model_ready": model_ready
        }

    except (
        error.URLError,
        TimeoutError,
        ValueError,
        OSError
    ):
        return {
            "provider": "ollama",
            "available": False,
            "models": [],
            "model_count": 0,
            "selected_model": selected_model,
            "model_ready": False
        }
