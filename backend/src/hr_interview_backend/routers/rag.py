from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from hr_interview_backend.database import get_db
from hr_interview_backend.schemas import RagDocumentResponse
from hr_interview_backend.services import rag_service

router = APIRouter()


@router.post("/documents", response_model=RagDocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        return await rag_service.upload_pdf(db, file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/documents", response_model=list[RagDocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return rag_service.list_documents(db)
