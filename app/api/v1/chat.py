import logging

from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import rag_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    """
    Ask questions to the RAG system.
    """

    try:
        answer = rag_service.answer(
            query=request.question
        )

        return ChatResponse(answer=answer)

    except Exception:
        logger.exception("Chat endpoint failed.")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate response.",
        )