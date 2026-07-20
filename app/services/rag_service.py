import logging
from typing import Any, Optional

from app.models.message import Message

from app.services.llm_service import llm_service
from app.services.prompt_builder import prompt_builder
from app.services.retriever_service import retriever_service

logger = logging.getLogger(__name__)


class RAGService:
    """
    Orchestrates the complete RAG pipeline.
    """

    def answer(
        self,
        query: str,
        conversation_history: Optional[list[Message]] = None,
        top_k: int = 5,
    ) -> dict[str, Any]:
        """
        Generate an answer using Retrieval-Augmented Generation.
        """

        logger.info("Starting RAG pipeline.")

        # ----------------------------------
        # Step 1: Retrieve relevant chunks
        # ----------------------------------

        retrieved_chunks = retriever_service.retrieve(
            query=query,
            top_k=top_k,
        )

        # ----------------------------------
        # Step 2: Build prompt
        # ----------------------------------

        prompt = prompt_builder.build_prompt(
            query=query,
            retrieved_chunks=retrieved_chunks,
            conversation_history=conversation_history,
        )

        # ----------------------------------
        # Step 3: Generate response
        # ----------------------------------

        answer = llm_service.generate(prompt)

        # ----------------------------------
        # Step 4: Build citations
        # ----------------------------------

        sources = []

        seen = set()

        for chunk in retrieved_chunks:

            metadata = chunk.get("metadata", {}) or {}

            source = {
                "document": metadata.get("filename", "Unknown"),
                "chunk_index": metadata.get("chunk_index"),
            }

            key = (
                source["document"],
                source["chunk_index"],
            )

            if key not in seen:
                seen.add(key)
                sources.append(source)

        logger.info("RAG pipeline completed.")

        return {
            "answer": answer,
            "sources": sources,
        }


rag_service = RAGService()