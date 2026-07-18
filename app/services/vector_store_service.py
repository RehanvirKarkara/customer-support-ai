import logging
from typing import Any

import chromadb
from chromadb.api.models.Collection import Collection

from app.core.config import settings

logger = logging.getLogger(__name__)


class VectorStoreService:
    """
    Handles all interactions with ChromaDB.

    Responsibilities:
    - Store document embeddings
    - Perform similarity search
    - Delete document chunks
    - Collection management
    """

    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH
        )

        self.collection: Collection = (
            self.client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION
            )
        )

        logger.info(
            "Connected to ChromaDB collection '%s'",
            settings.CHROMA_COLLECTION,
        )

    def add_documents(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
    ) -> None:
        """
        Store document chunks inside ChromaDB.
        """

        try:
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
            )

            logger.info(
                "Added %d documents to ChromaDB.",
                len(ids),
            )

        except Exception:
            logger.exception("Failed to add documents to ChromaDB.")
            raise

    def similarity_search(
        self,
        query_embedding: list[float],
        n_results: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Retrieve the most similar document chunks.
        """

        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
            )

            documents = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0]

            response = []

            for document, metadata, distance in zip(
                documents,
                metadatas,
                distances,
            ):
                response.append(
                    {
                        "document": document,
                        "metadata": metadata,
                        "score": distance,
                    }
                )

            return response

        except Exception:
            logger.exception("Similarity search failed.")
            raise

    def delete_document(
        self,
        document_id: str,
    ) -> None:
        """
        Delete all chunks belonging to one document.
        """

        try:
            self.collection.delete(
                where={
                    "document_id": document_id,
                }
            )

            logger.info(
                "Deleted document '%s' from ChromaDB.",
                document_id,
            )

        except Exception:
            logger.exception(
                "Failed to delete document '%s'.",
                document_id,
            )
            raise

    def count_documents(self) -> int:
        """
        Return the number of vectors currently stored.
        """

        return self.collection.count()

    def reset_collection(self) -> None:
        """
        Delete every vector inside the collection.
        Useful during development.
        """

        try:
            self.client.delete_collection(
                settings.CHROMA_COLLECTION
            )

            self.collection = (
                self.client.get_or_create_collection(
                    settings.CHROMA_COLLECTION
                )
            )

            logger.warning(
                "ChromaDB collection reset successfully."
            )

        except Exception:
            logger.exception(
                "Failed to reset ChromaDB collection."
            )
            raise


vector_store_service = VectorStoreService()