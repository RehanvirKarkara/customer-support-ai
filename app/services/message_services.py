from sqlalchemy.orm import Session

from app.models.message import Message

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository

from app.schemas.message import MessageCreate


class MessageService:

    def __init__(self, db: Session):
        self.message_repository = MessageRepository(db)
        self.conversation_repository = ConversationRepository(db)

    # -------------------------
    # Create Message
    # -------------------------

    def create_message(
        self,
        message_data: MessageCreate,
    ) -> Message:

        conversation = (
            self.conversation_repository
            .get_conversation_by_id(
                message_data.conversation_id
            )
        )

        if conversation is None:
            raise ValueError(
                "Conversation not found."
            )

        message = Message(
            conversation_id=message_data.conversation_id,
            sender=message_data.sender,
            content=message_data.content,
        )

        return self.message_repository.create_message(
            message
        )

    # -------------------------
    # Get Message
    # -------------------------

    def get_message(
        self,
        message_id: int,
    ) -> Message:

        message = (
            self.message_repository
            .get_message_by_id(message_id)
        )

        if message is None:
            raise ValueError(
                "Message not found."
            )

        return message

    # -------------------------
    # Get Conversation Messages
    # -------------------------

    def get_conversation_messages(
        self,
        conversation_id: int,
    ):

        conversation = (
            self.conversation_repository
            .get_conversation_by_id(
                conversation_id
            )
        )

        if conversation is None:
            raise ValueError(
                "Conversation not found."
            )

        return (
            self.message_repository
            .get_messages_by_conversation(
                conversation_id
            )
        )

    # -------------------------
    # Delete Message
    # -------------------------

    def delete_message(
        self,
        message_id: int,
    ):

        message = (
            self.message_repository
            .get_message_by_id(
                message_id
            )
        )

        if message is None:
            raise ValueError(
                "Message not found."
            )

        self.message_repository.delete_message(
            message
        )