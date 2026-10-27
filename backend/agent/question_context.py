
from agent.context_engine import build_related_context


def build_question_context(
    question: str,
    file_path: str,
    repository_path: str = "."
) -> dict:
    """
    Prepare repository context for a developer question.
    Does not call an AI model.
    """

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty")

    if len(question) > 2000:
        raise ValueError("Question is too long")

    related_context = build_related_context(
        file_path=file_path,
        repository_path=repository_path,
        max_files=5
    )

    return {
        "question": question,
        "context": related_context,
        "status": "context_ready"
    }
