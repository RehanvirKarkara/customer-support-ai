from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    conversation_id: int
    question: str = Field(..., min_length=1)


class SourceResponse(BaseModel):
    document: str
    chunk_index: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse] = []