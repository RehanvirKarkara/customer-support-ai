import logging
import uuid

from app.services.chunking_service import ChunkingService
from app.services.embedding_service import embedding_service
from app.services.pdf_service import PDFService
from app.services.vector_store_service import vector_store_service

logger = logging.getLogger(__name__)


class IngestionService:
    """
    Orchestrates the complete document ingestion pipeline.

    Pipeline:
        PDF
            ↓
        Extract Text
            ↓
        Split into Chunks
            ↓
        Generate Embeddings
            ↓
        Store in ChromaDB
    """

    def __init__(self) -> None:
        self.pdf_service = PDFService()
        self.chunking_service = ChunkingService()

    def ingest_pdf(
        self,
        file_path: str,
        filename: str,
    ) -> dict:
        """
        Ingest a PDF into the vector database.
        """

        logger.info(
            "Starting ingestion for '%s'.",
            filename,
        )

        # Step 1
        text = self.pdf_service.extract_text(
            file_path
        )

        # Step 2
        chunks = self.chunking_service.split_text(
            text
        )

        if not chunks:
            raise ValueError(
                "No text chunks generated from PDF."
            )

        # Step 3
        embeddings = (
            embedding_service.embed_documents(
                chunks
            )
        )

        document_id = str(uuid.uuid4())

        ids = []
        metadatas = []

        for index in range(len(chunks)):
            ids.append(str(uuid.uuid4()))

            metadatas.append(
                {
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_index": index,
                }
            )

        # Step 4
        vector_store_service.add_documents(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        logger.info(
            "Successfully ingested '%s' with %d chunks.",
            filename,
            len(chunks),
        )

        return {
            "document_id": document_id,
            "filename": filename,
            "chunks_created": len(chunks),
            "embeddings_created": len(embeddings),
        }


ingestion_service = IngestionService()