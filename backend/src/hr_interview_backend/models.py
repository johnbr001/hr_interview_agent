import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hr_interview_backend.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interviewer_name: Mapped[str] = mapped_column(String, nullable=False)
    candidate_name: Mapped[str] = mapped_column(String, nullable=False)
    role_title: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    turns: Mapped[list["ScoreTurn"]] = relationship(back_populates="session", cascade="all, delete-orphan")


class ScoreTurn(Base):
    __tablename__ = "score_turns"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("interview_sessions.id"))
    question_context: Mapped[str | None] = mapped_column(Text)
    interviewee_text: Mapped[str] = mapped_column(Text, nullable=False)
    grade: Mapped[str] = mapped_column(String(1), nullable=False)
    rationale: Mapped[str | None] = mapped_column(Text)
    scored_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    session: Mapped[InterviewSession] = relationship(back_populates="turns")


class RagDocument(Base):
    __tablename__ = "rag_documents"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    storage_path: Mapped[str] = mapped_column(String, nullable=False, default="")
    ingest_status: Mapped[str] = mapped_column(String, nullable=False, default="PENDING")
    chunk_count: Mapped[int | None] = mapped_column(Integer)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
