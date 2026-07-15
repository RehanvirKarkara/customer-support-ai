from sqlalchemy.orm import Session

from app.models.knowledge import Knowledge


class KnowledgeRepository:

    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # Create Knowledge
    # -------------------------

    def create_knowledge(
        self,
        knowledge: Knowledge,
    ) -> Knowledge:

        self.db.add(knowledge)
        self.db.commit()
        self.db.refresh(knowledge)

        return knowledge

    # -------------------------
    # Get By ID
    # -------------------------

    def get_by_id(
        self,
        knowledge_id: int,
    ):

        return (
            self.db.query(Knowledge)
            .filter(Knowledge.id == knowledge_id)
            .first()
        )

    # -------------------------
    # Get By File Name
    # -------------------------

    def get_by_file_name(
        self,
        file_name: str,
    ):

        return (
            self.db.query(Knowledge)
            .filter(Knowledge.file_name == file_name)
            .first()
        )

    # -------------------------
    # Get All Documents
    # -------------------------

    def get_all(self):

        return (
            self.db.query(Knowledge)
            .order_by(Knowledge.uploaded_at.desc())
            .all()
        )

    # -------------------------
    # Delete
    # -------------------------

    def delete(
        self,
        knowledge: Knowledge,
    ):

        self.db.delete(knowledge)
        self.db.commit()