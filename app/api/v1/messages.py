from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.message import (
    MessageCreate,
    MessageResponse,
)

from app.services.message_service import MessageService

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


# -------------------------
# Create Message
# -------------------------

@router.post(
    "/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
):

    service = MessageService(db)

    try:
        return service.create_message(message)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# -------------------------
# Get Message
# -------------------------

@router.get(
    "/{message_id}",
    response_model=MessageResponse,
)
def get_message(
    message_id: int,
    db: Session = Depends(get_db),
):

    service = MessageService(db)

    try:
        return service.get_message(message_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# -------------------------
# Get Conversation Messages
# -------------------------

@router.get(
    "/conversation/{conversation_id}",
    response_model=list[MessageResponse],
)
def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
):

    service = MessageService(db)

    try:
        return service.get_conversation_messages(
            conversation_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# -------------------------
# Delete Message
# -------------------------

@router.delete(
    "/{message_id}",
)
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
):

    service = MessageService(db)

    try:

        service.delete_message(message_id)

        return {
            "message": "Message deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )