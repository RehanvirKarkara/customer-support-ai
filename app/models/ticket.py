from enum import Enum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import relationship

from app.core.database import Base


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    priority: Mapped[TicketPriority] = mapped_column(
        SQLEnum(TicketPriority),
        default=TicketPriority.MEDIUM
    )

    status: Mapped[TicketStatus] = mapped_column(
        SQLEnum(TicketStatus),
        default=TicketStatus.OPEN
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    user = relationship(
        "User",
        back_populates="tickets"
    )


    def __repr__(self):
        return (
            f"<Ticket(id={self.id}, "
            f"title='{self.title}', "
            f"status='{self.status}')>"
        )
        
    conversation = relationship(
    "Conversation",
    back_populates="ticket",
    uselist=False,
    cascade="all, delete-orphan",)
        