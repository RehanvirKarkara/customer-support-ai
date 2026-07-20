from sqlalchemy.orm import Session

from app.models.message import Message


class MessageRepository:

    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # Create Message
    # -------------------------

    def create_message(
        self,
        message: Message,
    ) -> Message:

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    # -------------------------
    # Get Message By ID
    # -------------------------

    def get_message_by_id(
        self,
        message_id: int,
    ):

        return (
            self.db.query(Message)
            .filter(
                Message.id == message_id
            )
            .first()
        )

    # -------------------------
    # Get All Messages In A Conversation
    # -------------------------

    def get_messages_by_conversation(
        self,
        conversation_id: int,
    ):

        return (
            self.db.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .order_by(Message.created_at.asc())
            .all()
        )

    # -------------------------
    # Get Recent Messages
    # -------------------------

    def get_recent_messages(
        self,
        conversation_id: int,
        limit: int = 5,
    ):
        """
        Returns the latest messages from a conversation.

        We first fetch the newest messages,
        then reverse them so the AI receives them
        in chronological order.
        """

        messages = (
            self.db.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .order_by(
                Message.created_at.desc()
            )
            .limit(limit)
            .all()
        )

        return list(reversed(messages))

    # -------------------------
    # Delete Message
    # -------------------------

    def delete_message(
        self,
        message: Message,
    ):

        self.db.delete(message)
        self.db.commit()