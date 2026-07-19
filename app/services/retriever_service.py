import logging
from typing import Any

from app.services.embedding_service import embedding_service
from app.services.vector_store_service import vector_store_service

logger = logging.getLogger(__name__)


class RetrieverService:
    """
    Retrieves the most relevant document chunks
    for a user's query using semantic search.
    """

    def __init__(self) -> None:
        self.embedding_service = embedding_service
        self.vector_store = vector_store_service

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Retrieve the top-k most relevant chunks
        for a user's query.
        """

        try:
            logger.info(
                "Retrieving context for query: %s",
                query,
            )

            # Step 1
            query_embedding = (
                self.embedding_service.embed_query(query)
            )

            # Step 2
            results = (
                self.vector_store.similarity_search(
                    query_embedding=query_embedding,
                    n_results=top_k,
                )
            )

            logger.info(
                "Retrieved %d relevant chunks.",
                len(results),
            )

            return results

        except Exception:
            logger.exception(
                "Retriever service failed."
            )
            raise


retriever_service = RetrieverService()