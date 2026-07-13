from sqlalchemy.orm import Session

from app.models.conversation import Conversation


class ConversationRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_conversation(
        self,
        conversation: Conversation,
    ) -> Conversation:

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def get_conversation_by_id(
        self,
        conversation_id: int,
    ):

        return (
            self.db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

    def get_conversation_by_ticket(
        self,
        ticket_id: int,
    ):

        return (
            self.db.query(Conversation)
            .filter(
                Conversation.ticket_id == ticket_id
            )
            .first()
        )

    def delete_conversation(
        self,
        conversation: Conversation,
    ):

        self.db.delete(conversation)
        self.db.commit()