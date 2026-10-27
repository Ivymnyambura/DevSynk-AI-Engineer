
from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def analyze_code(
        self,
        issue: str,
        code: str
    ) -> dict:
        pass

    
    @abstractmethod
    def answer_question(
        self,
        question: str,
        context: dict
    ) -> dict:
        pass



class MockAIProvider(AIProvider):

    def analyze_code(
        self,
        issue: str,
        code: str
    ) -> dict:

        if not issue.strip():
            raise ValueError(
                "Issue description cannot be empty."
            )

        if not code.strip():
            raise ValueError(
                "Source code cannot be empty."
            )

        return {
            "provider": "mock",
            "status": "simulated",
            "issue_summary": issue,
            "severity": "unverified",
            "root_cause": (
                "Not determined. A real AI model "
                "is required for code analysis."
            ),
            "affected_files": [],
            "proposed_solution": {
                "description": (
                    "Placeholder solution for "
                    "development testing."
                ),
                "steps": [
                    "Inspect the reported issue.",
                    "Identify affected functions.",
                    "Develop a proposed fix.",
                    "Verify the fix with tests."
                ]
            },
            "suggested_tests": [
                "Normal input test",
                "Edge case test",
                "Error handling test"
            ],
            "verification": {
                "tests_executed": False,
                "result": "not_run"
            },
            "code_length": len(code)
        }
    
    def answer_question(
        self,
        question: str,
        context: dict
    ) -> dict:

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        files = context.get("files", [])

        if not files:
            raise ValueError("Repository context is empty.")

        file_names = [
            file["file"]
            for file in files
        ]

        return {
            "provider": "mock",
            "status": "simulated",
            "answer": (
                "Repository context was prepared successfully "
                "for the requested developer question. "
                "A real AI provider has not been connected yet."
            ),
            "context_files": file_names,
            "total_context_files": len(file_names)
        }

