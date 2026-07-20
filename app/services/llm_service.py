import logging

from google import genai

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """
    Handles communication with Gemini.
    """

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.model = settings.GEMINI_CHAT_MODEL

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate an answer using Gemini.
        """

        try:
            logger.info("Sending prompt to Gemini...")

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            logger.info("Gemini response received.")

            return response.text

        except Exception:
            logger.exception("LLM generation failed.")
            raise


llm_service = LLMService()