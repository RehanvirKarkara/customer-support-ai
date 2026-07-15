from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class KnowledgeStatus(str, Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"


class KnowledgeCreate(BaseModel):
    title: str


class KnowledgeResponse(BaseModel):
    id: int
    title: str
    file_name: str
    file_path: str
    status: KnowledgeStatus
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }