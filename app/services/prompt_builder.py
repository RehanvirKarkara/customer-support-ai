from typing import Any


class PromptBuilder:
    """
    Builds prompts for the LLM using
    retrieved document context.
    """

    SYSTEM_PROMPT = """
You are an AI customer support assistant for Airtel.

Your responsibilities:

- Answer ONLY using the provided context.
- If the answer is not present in the context, clearly say:
  "I couldn't find that information in the uploaded documents."
- Do not make up information.
- Keep answers concise, professional, and accurate.
"""

    def build_prompt(
        self,
        query: str,
        retrieved_chunks: list[dict[str, Any]],
    ) -> str:
        """
        Build the final prompt that will
        be sent to the LLM.
        """

        context = "\n\n".join(
            chunk["document"]
            for chunk in retrieved_chunks
        )

        prompt = f"""
{self.SYSTEM_PROMPT}

Context:
--------------------
{context}

--------------------

Question:
{query}

Answer:
"""

        return prompt


prompt_builder = PromptBuilder()