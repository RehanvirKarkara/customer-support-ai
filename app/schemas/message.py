from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class MessageSender(str, Enum):
    USER = "USER"
    AI = "AI"


# -------------------------
# Create Message
# -------------------------

class MessageCreate(BaseModel):
    conversation_id: int
    sender: MessageSender
    content: str = Field(..., min_length=1)


# -------------------------
# Response
# -------------------------

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender: MessageSender
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }