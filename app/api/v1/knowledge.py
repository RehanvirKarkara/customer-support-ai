from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.knowledge import (
    KnowledgeCreate,
    KnowledgeResponse,
)

from app.services.knowledge_service import (
    KnowledgeService,
)

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge"],
)


UPLOAD_DIRECTORY = Path("uploads")
UPLOAD_DIRECTORY.mkdir(exist_ok=True)


# -------------------------
# Upload Document
# -------------------------

@router.post(
    "/upload",
    response_model=KnowledgeResponse,
)
async def upload_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    file_path = (
        UPLOAD_DIRECTORY / file.filename
    )

    with open(file_path, "wb") as pdf:
        pdf.write(
            await file.read()
        )

    service = KnowledgeService(db)

    try:

        knowledge = service.create_knowledge(
            KnowledgeCreate(title=title),
            file_name=file.filename,
            file_path=str(file_path),
        )

        return knowledge

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )