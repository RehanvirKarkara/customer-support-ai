from langchain_community.embeddings import OllamaEmbeddings


class EmbeddingService:
    """
    Generates vector embeddings from text chunks.
    """

    def __init__(self):
        self.embedding_model = OllamaEmbeddings(
            model="nomic-embed-text:v1.5"
        )

    def embed_chunks(
        self,
        chunks: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for a list of chunks.
        """

        return self.embedding_model.embed_documents(
            chunks
        )

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate embedding for a user's question.
        """

        return self.embedding_model.embed_query(
            query
        )