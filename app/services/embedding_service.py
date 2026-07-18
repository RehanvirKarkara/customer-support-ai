import logging

from google import genai

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Handles all embedding operations using the Gemini Embedding API.
    """

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_EMBEDDING_MODEL

        logger.info(
            "Initialized Gemini Embedding Service with model '%s'.",
            self.model,
        )

    def _embed(
        self,
        texts: list[str],
        task_type: str,
    ) -> list[list[float]]:
        """
        Internal helper for generating embeddings.
        """

        if not texts:
            return []

        try:
            response = self.client.models.embed_content(
                model=self.model,
                contents=texts,
                config={
                    "task_type": task_type,
                },
            )

            embeddings = [
                embedding.values
                for embedding in response.embeddings
            ]

            logger.info(
                "Generated %d embedding(s).",
                len(embeddings),
            )

            return embeddings

        except Exception:
            logger.exception(
                "Failed to generate embeddings."
            )
            raise

    def embed_documents(
        self,
        documents: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for document chunks.
        """

        return self._embed(
            texts=documents,
            task_type="RETRIEVAL_DOCUMENT",
        )

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate embedding for a user query.
        """

        embeddings = self._embed(
            texts=[query],
            task_type="RETRIEVAL_QUERY",
        )

        return embeddings[0]


embedding_service = EmbeddingService()