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

from app.services.ingestion_service import (
    ingestion_service,
)

from app.services.vector_store_service import (
    vector_store_service,
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

    file_path = UPLOAD_DIRECTORY / file.filename

    with open(file_path, "wb") as pdf:
        pdf.write(await file.read())

    service = KnowledgeService(db)

    try:

        knowledge = service.create_knowledge(
            KnowledgeCreate(title=title),
            file_name=file.filename,
            file_path=str(file_path),
        )
        
        # Index the uploaded PDF into ChromaDB
        ingestion_service.ingest_pdf(
            file_path=str(file_path),
            filename=file.filename,
        )

        return knowledge

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# -------------------------
# Get All Documents
# -------------------------

@router.get(
    "/",
    response_model=list[KnowledgeResponse],
)
def get_all_documents(
    db: Session = Depends(get_db),
):

    service = KnowledgeService(db)

    return service.get_all_documents()


# -------------------------
# Delete Document
# -------------------------

@router.delete("/{knowledge_id}")
def delete_document(
    knowledge_id: int,
    db: Session = Depends(get_db),
):

    service = KnowledgeService(db)

    try:

        service.delete_document(knowledge_id)

        return {
            "message": "Knowledge document deleted successfully."
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


# -------------------------
# Reset ChromaDB (Development Only)
# -------------------------

@router.post("/reset")
def reset_knowledge():

    vector_store_service.reset_collection()

    return {
        "message": "ChromaDB reset successfully."
    }