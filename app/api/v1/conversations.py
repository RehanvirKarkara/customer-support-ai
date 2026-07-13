from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
)
from app.services.conversation_service import ConversationService

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


# -------------------------
# Create Conversation
# -------------------------
@router.post(
    "/",
    response_model=ConversationResponse,
)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)

    try:
        return service.create_conversation(
            conversation.ticket_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# -------------------------
# Get Conversation
# -------------------------
@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)

    try:
        return service.get_conversation(
            conversation_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


# -------------------------
# Delete Conversation
# -------------------------
@router.delete(
    "/{conversation_id}",
)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)

    try:
        service.delete_conversation(
            conversation_id
        )

        return {
            "message": "Conversation deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )