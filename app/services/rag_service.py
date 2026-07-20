import logging

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
        top_k: int = 5,
    ) -> str:
        """
        Generate an answer using Retrieval-Augmented Generation.
        """

        logger.info("Starting RAG pipeline.")

        # Step 1: Retrieve relevant chunks
        retrieved_chunks = retriever_service.retrieve(
            query=query,
            top_k=top_k,
        )

        # Step 2: Build prompt
        prompt = prompt_builder.build_prompt(
            query=query,
            retrieved_chunks=retrieved_chunks,
        )

        # Step 3: Generate response
        answer = llm_service.generate(prompt)

        logger.info("RAG pipeline completed.")

        return answer


rag_service = RAGService()