from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from hr_interview_backend.models import InterviewSession, ScoreTurn
from hr_interview_backend.schemas import (
    CreateSessionRequest,
    ScoreRequest,
    ScoreTurnResponse,
    SessionResponse,
)
from hr_interview_backend import temporal_service


def create_session(db: Session, request: CreateSessionRequest) -> SessionResponse:
    session = InterviewSession(
        interviewer_name=request.interviewer_name,
        candidate_name=request.candidate_name,
        role_title=request.role_title,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return SessionResponse.model_validate(session)


def get_session(db: Session, session_id: UUID) -> SessionResponse:
    session = db.get(InterviewSession, session_id)
    if session is None:
        raise ValueError(f"Session not found: {session_id}")
    return SessionResponse.model_validate(session)


async def score(db: Session, session_id: UUID, request: ScoreRequest) -> ScoreTurnResponse:
    session = db.get(InterviewSession, session_id)
    if session is None:
        raise ValueError("Session not found")

    ai = await temporal_service.score_turn(
        session_id,
        request.interviewee_text,
        request.question_context,
        request.use_web_search,
    )

    turn = ScoreTurn(
        session_id=session_id,
        question_context=request.question_context,
        interviewee_text=request.interviewee_text,
        grade=ai["grade"],
        rationale=ai["rationale"],
    )
    db.add(turn)
    db.commit()
    db.refresh(turn)
    return ScoreTurnResponse.model_validate(turn)


def list_turns(db: Session, session_id: UUID) -> list[ScoreTurnResponse]:
    stmt = (
        select(ScoreTurn)
        .where(ScoreTurn.session_id == session_id)
        .order_by(ScoreTurn.scored_at.asc())
    )
    turns = db.scalars(stmt).all()
    return [ScoreTurnResponse.model_validate(t) for t in turns]
