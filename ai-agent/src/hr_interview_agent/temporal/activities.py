from temporalio import activity

from hr_interview_agent.graph.scorer import score_interview_turn
from hr_interview_agent.rag.store import ingest_pdf


@activity.defn(name="ScoreInterviewTurn")
async def score_interview_turn_activity(
    session_id: str,
    interviewee_text: str,
    question_context: str,
    use_web_search: bool,
) -> dict:
    return await score_interview_turn(
        session_id=session_id,
        interviewee_text=interviewee_text,
        question_context=question_context,
        use_web_search=use_web_search,
    )


@activity.defn(name="IngestPdfRag")
async def ingest_pdf_rag_activity(file_path: str, document_id: str) -> int:
    return ingest_pdf(file_path, document_id)
