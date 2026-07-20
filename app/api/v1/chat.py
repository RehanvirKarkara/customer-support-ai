import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.message import MessageCreate, MessageSender

from app.services.message_service import MessageService
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
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Chat endpoint with conversation memory.
    """

    try:

        message_service = MessageService(db)

        # -----------------------------------
        # Step 1: Get Previous Conversation
        # -----------------------------------

        conversation_history = (
            message_service.get_recent_messages(
                conversation_id=request.conversation_id,
                limit=5,
            )
        )

        # -----------------------------------
        # Step 2: Generate AI Response
        # -----------------------------------

        result = rag_service.answer(
            query=request.question,
            conversation_history=conversation_history,
        )

        # -----------------------------------
        # Step 3: Save User Message
        # -----------------------------------

        message_service.create_message(
            MessageCreate(
                conversation_id=request.conversation_id,
                sender=MessageSender.USER,
                content=request.question,
            )
        )

        # -----------------------------------
        # Step 4: Save AI Message
        # -----------------------------------

        message_service.create_message(
            MessageCreate(
                conversation_id=request.conversation_id,
                sender=MessageSender.AI,
                content=result["answer"],
            )
        )

        # -----------------------------------
        # Step 5: Return Response
        # -----------------------------------

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
        )

    except Exception:
        logger.exception(
            "Chat endpoint failed."
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to generate response.",
        )