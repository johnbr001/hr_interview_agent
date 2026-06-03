"""MCP-style tool adapters for the LangGraph agent.

In production, run dedicated MCP servers (see mcp/servers/) and connect via
the MCP Python SDK. This module provides the same contracts for local/dev.
"""

import json
from typing import Any

import httpx

from hr_interview_agent.config import settings


async def web_search(query: str, max_results: int = 5) -> str:
    """Search the web via Tavily (preferred) or Brave Search API."""
    if settings.tavily_api_key:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": settings.tavily_api_key,
                    "query": query,
                    "max_results": max_results,
                    "search_depth": "basic",
                },
            )
            resp.raise_for_status()
            data = resp.json()
            lines = []
            for r in data.get("results", []):
                lines.append(f"- {r.get('title')}: {r.get('content', '')[:400]}")
            return "\n".join(lines) if lines else "No results."

    if settings.brave_api_key:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={"X-Subscription-Token": settings.brave_api_key},
                params={"q": query, "count": max_results},
            )
            resp.raise_for_status()
            data = resp.json()
            lines = []
            for r in data.get("web", {}).get("results", []):
                lines.append(f"- {r.get('title')}: {r.get('description', '')}")
            return "\n".join(lines) if lines else "No results."

    return "Web search unavailable (set TAVILY_API_KEY or BRAVE_API_KEY)."


def database_lookup(session_id: str, question_key: str | None = None) -> str:
    """Placeholder for MCP database server — backend owns canonical DB."""
    payload: dict[str, Any] = {
        "session_id": session_id,
        "question_key": question_key,
        "note": "Use Spring backend /api/sessions for authoritative history.",
    }
    return json.dumps(payload)
