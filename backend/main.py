from pydantic import BaseModel
from agent.ai_config import get_ai_config
from agent.ollama_health import check_ollama_health
from agent.answer_engine import generate_developer_answer
from agent.question_context import build_question_context
from agent.context_engine import build_file_context
from agent.repository_intelligence import analyze_repository
from agent.code_inspector import inspect_python_code
from agent.ai_provider import MockAIProvider
from fastapi import FastAPI
from agent.repository import (
    list_repository_files,
    read_repository_file
)
from fastapi import HTTPException
from agent.dependency_analyzer import (
    find_dependent_files,
    find_all_dependent_files,
)

class AnalysisRequest(BaseModel):
    issue: str
    file_path: str


class QuestionContextRequest(BaseModel):
    question: str
    file_path: str


app = FastAPI(
    title="DevSynk AI Engineer API",
    description="AI-powered software engineering agent",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to DevSynk AI Engineer!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "DevSynk AI Engineer Backend"
    }


@app.get("/repository/files")
def get_repository_files():
    files = list_repository_files(".")

    return {
        "repository": "DevSynk AI Engineer Backend",
        "total_files": len(files),
        "files": files
    }


@app.get("/repository/file")
def get_repository_file(path: str):
    try:
        content = read_repository_file(".", path)

        return {
            "file": path,
            "content": content
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@app.post("/agent/analyze")
def analyze_repository_code(request: AnalysisRequest):
    try:
        code = read_repository_file(
            ".",
            request.file_path
        )

        provider = MockAIProvider()

        
        ai_result = provider.analyze_code(
            issue=request.issue,
            code=code
        )

        inspection = None

        if request.file_path.lower().endswith(".py"):
            inspection = inspect_python_code(code)

        return {
            "file": request.file_path,
            "ai_analysis": ai_result,
            "code_inspection": inspection
        }


    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@app.get("/repository/analyze")
def analyze_repository_endpoint():
    """
    Analyze the local repository and return
    structured source code inspection results.
    """

    return analyze_repository(".")


@app.get("/repository/impact")
def analyze_file_impact(path: str):
    """
    Find repository files that directly or indirectly
    depend on the requested file.
    """

    repository = analyze_repository(".")

    available_files = {
        item["file"] for item in repository["files"]
    }

    if path not in available_files:
        raise HTTPException(
            status_code=404,
            detail="File not found in analyzed repository"
        )

    analyzed_files = repository["files"]

    direct_dependents = find_dependent_files(
        path,
        analyzed_files
    )

    all_dependents = find_all_dependent_files(
        path,
        analyzed_files
    )

    return {
        "file": path,
        "direct_dependents": direct_dependents,
        "indirect_dependents": [
            file for file in all_dependents
            if file not in direct_dependents
        ],
        "total_affected_files": len(all_dependents)
    }


@app.get("/repository/context")
def get_repository_context(path: str):
    """
    Return source code, inspection results,
    and dependency information for a repository file.
    """

    try:
        return build_file_context(
            file_path=path,
            repository_path="."
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error


@app.post("/agent/question/context")
def prepare_question_context(request: QuestionContextRequest):
    """
    Prepare repository context for a developer question.
    Does not call an AI model.
    """

    try:
        return build_question_context(
            question=request.question,
            file_path=request.file_path,
            repository_path="."
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error


@app.post("/agent/question/answer")
def answer_developer_question(request: QuestionContextRequest):
    """
    Generate an answer using repository context.

    Currently uses a simulated AI response.
    """

    try:
        return generate_developer_answer(
            question=request.question,
            file_path=request.file_path,
            repository_path="."
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error


@app.get("/ai/providers/ollama/status")
def get_ollama_status():
    """
    Return local Ollama availability and installed models.
    """
    return check_ollama_health()


@app.get("/ai/provider/status")
def get_ai_provider_status():
    """
    Return safe configuration information about
    the currently selected AI provider.
    """
    config = get_ai_config()

    return {
        "provider": config["provider"],
        "configured": config["configured"],
        "supported_providers": config["supported_providers"],
        "status": (
            "configured"
            if config["configured"]
            else "configuration_required"
        )
    }
