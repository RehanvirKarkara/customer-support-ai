from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.ticket import Ticket

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.ticket_repository import TicketRepository


class ConversationService:

    def __init__(self, db: Session):
        self.conversation_repository = ConversationRepository(db)
        self.ticket_repository = TicketRepository(db)

    def create_conversation(
        self,
        ticket_id: int,
    ) -> Conversation:

        ticket = self.ticket_repository.get_ticket_by_id(ticket_id)

        if not ticket:
            raise ValueError("Ticket not found.")

        existing = (
            self.conversation_repository
            .get_conversation_by_ticket(ticket_id)
        )

        if existing:
            raise ValueError(
                "Conversation already exists for this ticket."
            )

        conversation = Conversation(
            ticket_id=ticket_id
        )

        return self.conversation_repository.create_conversation(
            conversation
        )

    def get_conversation(
        self,
        conversation_id: int,
    ) -> Conversation:

        conversation = (
            self.conversation_repository
            .get_conversation_by_id(conversation_id)
        )

        if not conversation:
            raise ValueError("Conversation not found.")

        return conversation

    def delete_conversation(
        self,
        conversation_id: int,
    ):

        conversation = (
            self.conversation_repository
            .get_conversation_by_id(conversation_id)
        )

        if not conversation:
            raise ValueError("Conversation not found.")

        self.conversation_repository.delete_conversation(
            conversation
        )