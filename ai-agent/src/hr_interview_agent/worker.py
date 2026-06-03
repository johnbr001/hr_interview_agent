"""Temporal worker — run: python -m hr_interview_agent.worker"""

import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from hr_interview_agent.config import settings
from hr_interview_agent.temporal.activities import (
    ingest_pdf_rag_activity,
    score_interview_turn_activity,
)
from hr_interview_agent.temporal.workflows import (
    IngestRagDocumentWorkflow,
    InterviewScoringWorkflow,
)


async def main() -> None:
    client = await Client.connect(
        settings.temporal_host,
        namespace=settings.temporal_namespace,
    )
    worker = Worker(
        client,
        task_queue=settings.temporal_task_queue,
        workflows=[InterviewScoringWorkflow, IngestRagDocumentWorkflow],
        activities=[score_interview_turn_activity, ingest_pdf_rag_activity],
    )
    print(f"HR Interview worker on queue={settings.temporal_task_queue}")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
