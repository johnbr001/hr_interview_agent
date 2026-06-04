from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from hr_interview_backend.database import get_db
from hr_interview_backend.schemas import (
    CreateSessionRequest,
    ScoreRequest,
    ScoreTurnResponse,
    SessionResponse,
)
from hr_interview_backend.services import interview_service

router = APIRouter()


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(request: CreateSessionRequest, db: Session = Depends(get_db)):
    return interview_service.create_session(db, request)


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: UUID, db: Session = Depends(get_db)):
    try:
        return interview_service.get_session(db, session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/{session_id}/score", response_model=ScoreTurnResponse)
async def score(session_id: UUID, request: ScoreRequest, db: Session = Depends(get_db)):
    try:
        return await interview_service.score(db, session_id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{session_id}/turns", response_model=list[ScoreTurnResponse])
def list_turns(session_id: UUID, db: Session = Depends(get_db)):
    return interview_service.list_turns(db, session_id)
