from sqlalchemy.orm import Session
import os

from app.models.knowledge import (
    Knowledge,
    KnowledgeStatus,
)

from app.repositories.knowledge_repository import (
    KnowledgeRepository,
)

from app.schemas.knowledge import KnowledgeCreate


class KnowledgeService:

    def __init__(self, db: Session):
        self.repository = KnowledgeRepository(db)

    # -------------------------
    # Create Knowledge
    # -------------------------

    def create_knowledge(
        self,
        knowledge_data: KnowledgeCreate,
        file_name: str,
        file_path: str,
    ) -> Knowledge:

        existing = self.repository.get_by_file_name(
            file_name
        )

        if existing:
            raise ValueError(
                "A document with this filename already exists."
            )

        knowledge = Knowledge(
            title=knowledge_data.title,
            file_name=file_name,
            file_path=file_path,
            status=KnowledgeStatus.UPLOADED,
        )

        return self.repository.create_knowledge(
            knowledge
        )

    # -------------------------
    # Get By ID
    # -------------------------

    def get_knowledge(
        self,
        knowledge_id: int,
    ) -> Knowledge:

        knowledge = self.repository.get_by_id(
            knowledge_id
        )

        if knowledge is None:
            raise ValueError(
                "Knowledge document not found."
            )

        return knowledge

    # -------------------------
    # Get All
    # -------------------------

    def get_all_documents(self):

        return self.repository.get_all()

    # -------------------------
    # Delete
    # -------------------------

    def delete_document(
        self,
        knowledge_id: int,
    ):

        knowledge = self.repository.get_by_id(
            knowledge_id
        )

        if knowledge is None:
            raise ValueError(
                "Knowledge document not found."
            )

        # Delete file from disk
        if (
            knowledge.file_path
            and os.path.exists(knowledge.file_path)
        ):
            os.remove(knowledge.file_path)

        # Delete database record
        self.repository.delete(
            knowledge
        )