
from fastapi import FastAPI
from agent.repository import (
    list_repository_files,
    read_repository_file
)
from fastapi import HTTPException

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

