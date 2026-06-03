# HR Interview System — Architecture

## Request flow (score one answer)

1. Interviewer submits text in React UI.
2. Spring `POST /api/sessions/{id}/score` persists intent and starts Temporal workflow `InterviewScoringWorkflow`.
3. Python worker executes LangGraph:
   - **retrieve_rag**: Chroma similarity search over ingested PDF chunks.
   - **maybe_web_search**: Tavily/Brave via MCP adapter (optional checkbox).
   - **score_answer**: ChatGPT returns JSON `{ grade, rationale }`.
4. Backend saves `ScoreTurn` and returns grade to UI.

## Why Temporal?

- Retries and timeouts for LLM calls (minutes-long activities).
- Same workflow for PDF ingest (`IngestRagDocumentWorkflow`).
- Future: multi-step interviews, human-in-the-loop, scheduled reports.

## Why MCP?

Tools are isolated processes with standard protocols:

- Swap Brave ↔ Tavily without changing LangGraph.
- Postgres MCP for read-only history without embedding SQL in prompts.
- Filesystem MCP for secure PDF paths on SCP volumes.

Dev mode uses `ai-agent/src/hr_interview_agent/mcp/tools.py` with the same interfaces.

## RAG design

- Upload PDF via backend → stored on volume → Temporal activity chunks + embeds into Chroma.
- Each scoring turn retrieves top-k chunks conditioned on question + answer text.
- Use structured Q&A PDFs (clear headings) for best retrieval.

## Security notes (production)

- Authenticate interviewers (SSO / Samsung IAM).
- Encrypt secrets via SCP Secret Manager.
- Network policies: only backend ↔ Temporal ↔ worker; no public worker endpoint.
- Audit log all scores and prompts.
