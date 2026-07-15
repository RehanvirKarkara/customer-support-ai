from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkingService:
    """
    Splits extracted text into chunks suitable for embeddings.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split_text(self, text: str) -> list[str]:
        """
        Split text into overlapping chunks.
        """
        return self.text_splitter.split_text(text)