from uuid import UUID, uuid4

from temporalio.client import Client

from hr_interview_backend.config import settings

_client: Client | None = None


async def get_temporal_client() -> Client:
    global _client
    if _client is None:
        _client = await Client.connect(
            settings.temporal_host,
            namespace=settings.temporal_namespace,
        )
    return _client


async def close_temporal_client() -> None:
    global _client
    if _client is not None:
        await _client.close()
        _client = None


async def score_turn(
    session_id: UUID,
    interviewee_text: str,
    question_context: str | None,
    use_web_search: bool,
) -> dict[str, str]:
    from hr_interview_agent.temporal.workflows import InterviewScoringWorkflow

    client = await get_temporal_client()
    result = await client.execute_workflow(
        InterviewScoringWorkflow.run,
        str(session_id),
        interviewee_text,
        question_context or "",
        use_web_search,
        id=f"score-{session_id}-{uuid4()}",
        task_queue=settings.temporal_task_queue,
    )
    return {
        "grade": str(result.get("grade", "C")),
        "rationale": str(result.get("rationale", "")),
    }


async def ingest_rag_document(file_path: str, document_id: UUID) -> int:
    from hr_interview_agent.temporal.workflows import IngestRagDocumentWorkflow

    client = await get_temporal_client()
    return await client.execute_workflow(
        IngestRagDocumentWorkflow.run,
        file_path,
        str(document_id),
        id=f"ingest-{document_id}",
        task_queue=settings.temporal_task_queue,
    )
