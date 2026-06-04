from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


def _to_camel(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


class CamelModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=_to_camel,
        from_attributes=True,
    )


class CreateSessionRequest(CamelModel):
    interviewer_name: str = Field(min_length=1)
    candidate_name: str = Field(min_length=1)
    role_title: str | None = None


class SessionResponse(CamelModel):
    id: UUID
    interviewer_name: str
    candidate_name: str
    role_title: str | None
    created_at: datetime


class ScoreRequest(CamelModel):
    interviewee_text: str = Field(min_length=1)
    question_context: str | None = None
    use_web_search: bool = False


class ScoreTurnResponse(CamelModel):
    id: UUID
    question_context: str | None
    interviewee_text: str
    grade: str
    rationale: str | None
    scored_at: datetime


class RagDocumentResponse(CamelModel):
    id: UUID
    file_name: str
    storage_path: str
    ingest_status: str
    chunk_count: int | None
    uploaded_at: datetime
