from agent.context_safety import validate_ai_context
from agent.ai_provider import AIProvider
from agent.provider_factory import create_ai_provider
from agent.question_context import build_question_context


def generate_developer_answer(
    question: str,
    file_path: str,
    repository_path: str = ".",
    provider: AIProvider | None = None
) -> dict:
    """
    Prepare repository context and request an answer
    from the configured AI provider.

    Defaults to MockAIProvider for local development.
    """

    prepared = build_question_context(
        question=question,
        file_path=file_path,
        repository_path=repository_path
    )

    active_provider = (
    provider if provider is not None
    else create_ai_provider()
    )

    
    safe_context = validate_ai_context(
        prepared["context"]
    )

    result = active_provider.answer_question(
        question=prepared["question"],
        context=safe_context
    )


    return {
        "question": prepared["question"],
        **result
    }
