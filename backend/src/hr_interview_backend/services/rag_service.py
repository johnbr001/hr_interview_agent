from pathlib import Path
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from hr_interview_backend.config import settings
from hr_interview_backend.models import RagDocument
from hr_interview_backend.schemas import RagDocumentResponse
from hr_interview_backend import temporal_service

_upload_dir = Path(settings.rag_upload_dir)


def _ensure_upload_dir() -> Path:
    _upload_dir.mkdir(parents=True, exist_ok=True)
    return _upload_dir


async def upload_pdf(db: Session, file: UploadFile) -> RagDocumentResponse:
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported")

    doc = RagDocument(file_name=filename, storage_path="")
    db.add(doc)
    db.commit()
    db.refresh(doc)

    dest = _ensure_upload_dir() / f"{doc.id}.pdf"
    content = await file.read()
    dest.write_bytes(content)
    doc.storage_path = str(dest.resolve())

    try:
        chunks = await temporal_service.ingest_rag_document(doc.storage_path, doc.id)
        doc.chunk_count = chunks
        doc.ingest_status = "READY"
    except Exception:
        doc.ingest_status = "FAILED"
        db.commit()
        raise

    db.commit()
    db.refresh(doc)
    return RagDocumentResponse.model_validate(doc)


def list_documents(db: Session) -> list[RagDocumentResponse]:
    docs = db.query(RagDocument).order_by(RagDocument.uploaded_at.desc()).all()
    return [RagDocumentResponse.model_validate(d) for d in docs]
