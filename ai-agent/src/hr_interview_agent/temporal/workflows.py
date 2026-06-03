from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from hr_interview_agent.temporal.activities import (
        ingest_pdf_rag_activity,
        score_interview_turn_activity,
    )


@workflow.defn(name="InterviewScoringWorkflow")
class InterviewScoringWorkflow:
    """Orchestrates a single scoring turn: RAG + optional web + LLM grade."""

    @workflow.run
    async def run(
        self,
        session_id: str,
        interviewee_text: str,
        question_context: str = "",
        use_web_search: bool = False,
    ) -> dict:
        return await workflow.execute_activity(
            score_interview_turn_activity,
            args=[session_id, interviewee_text, question_context, use_web_search],
            start_to_close_timeout=timedelta(minutes=3),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )


@workflow.defn(name="IngestRagDocumentWorkflow")
class IngestRagDocumentWorkflow:
    @workflow.run
    async def run(self, file_path: str, document_id: str) -> int:
        return await workflow.execute_activity(
            ingest_pdf_rag_activity,
            args=[file_path, document_id],
            start_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(maximum_attempts=2),
        )
