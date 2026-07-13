from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# -------------------------
# Enums
# -------------------------

class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


# -------------------------
# Create Ticket
# -------------------------

class TicketCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    priority: TicketPriority = TicketPriority.MEDIUM


# -------------------------
# Update Ticket
# -------------------------

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TicketPriority] = None
    status: Optional[TicketStatus] = None


# -------------------------
# Response
# -------------------------

class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: TicketPriority
    status: TicketStatus
    user_id: int

    model_config = {
        "from_attributes": True
    }