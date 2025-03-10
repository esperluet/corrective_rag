from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from repository.article_repository import ArticleRepository
from workflow.graph import run_workflow

router = APIRouter()

article_repository = ArticleRepository()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_question(request: QuestionRequest):
    """
    Executes the RAG workflow for the given question.
    """
    try:
        final_state = run_workflow(request.question, article_repository)
        return {
            "answer": final_state["generation"],
            "steps": final_state["steps"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
