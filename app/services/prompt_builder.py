from typing import Any

from app.models.message import Message


class PromptBuilder:
    """
    Builds prompts for the LLM using:

    - Conversation History
    - Retrieved Context
    - Current Question
    """

    SYSTEM_PROMPT = """
You are an AI customer support assistant for Airtel.

Your responsibilities:

- Answer ONLY using the provided context.
- Use the conversation history to understand follow-up questions.
- If the answer is not present in the context, clearly say:
  "I couldn't find that information in the uploaded documents."
- Do not make up information.
- Keep answers concise, professional, and accurate.
"""

    def build_prompt(
        self,
        query: str,
        retrieved_chunks: list[dict[str, Any]],
        conversation_history: list[Message] | None = None,
    ) -> str:

        # -------------------------
        # Build Knowledge Context
        # -------------------------

        context = "\n\n".join(
            chunk["document"]
            for chunk in retrieved_chunks
        )

        # -------------------------
        # Build Conversation History
        # -------------------------

        history = ""

        if conversation_history:

            history_lines = []

            for message in conversation_history:

                history_lines.append(
                    f"{message.sender.value}: {message.content}"
                )

            history = "\n".join(history_lines)

        else:

            history = "No previous conversation."

        # -------------------------
        # Final Prompt
        # -------------------------

        prompt = f"""
{self.SYSTEM_PROMPT}

Conversation History:
--------------------
{history}

--------------------

Knowledge Base Context:
--------------------
{context}

--------------------

Current Question:
{query}

Answer:
"""

        return prompt


prompt_builder = PromptBuilder()