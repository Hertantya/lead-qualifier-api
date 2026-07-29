from fastapi import APIRouter

from app.models import AskRequest, AskResponse
from app.rag.qa import ask as rag_ask

router = APIRouter(tags=["rag"])


@router.post("/ask", response_model=AskResponse)
def ask_endpoint(req: AskRequest) -> AskResponse:
    return rag_ask(req.question, top_k=req.top_k)
