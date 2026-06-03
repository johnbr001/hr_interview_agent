# MCP Servers for HR Interview Agent

Run these as separate processes; the LangGraph agent connects via MCP stdio/SSE.

| Server | Purpose | Suggested package |
|--------|---------|-------------------|
| `web-search` | Internet search for role/industry context | `@modelcontextprotocol/server-brave-search` or Tavily MCP |
| `postgres` | Read interview history / rubrics | `@modelcontextprotocol/server-postgres` |
| `filesystem` | Read uploaded PDFs before ingest | `@modelcontextprotocol/server-filesystem` |

## Example: Brave web search

```bash
npx -y @modelcontextprotocol/server-brave-search
# env: BRAVE_API_KEY
```

## Example: Postgres (read-only user)

```bash
npx -y @modelcontextprotocol/server-postgres "postgresql://hr:hr_secret@localhost:5432/hr_interview"
```

Wire MCP clients in `graph/scorer.py` when moving from dev adapters (`mcp/tools.py`) to production MCP transports.
