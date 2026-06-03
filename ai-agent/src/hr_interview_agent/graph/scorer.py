"""LangGraph workflow: RAG retrieve → optional web search → grade."""

import json
import re
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from hr_interview_agent.config import settings
from hr_interview_agent.graph.state import Grade, InterviewState
from hr_interview_agent.mcp.tools import web_search
from hr_interview_agent.rag.store import retrieve_context

SYSTEM_PROMPT = """You are an expert HR interview evaluator.
Score the interviewee's answer using the reference Q&A material when provided.
Assign exactly one letter grade: A (excellent), B (good), C (adequate), D (weak), F (fail).
Respond ONLY with valid JSON:
{"grade": "A|B|C|D|F", "rationale": "2-4 sentences explaining the score"}
"""


def _llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0.2,
    )


async def retrieve_rag(state: InterviewState) -> dict[str, Any]:
    query = f"{state.get('question_context', '')} {state['interviewee_text']}".strip()
    ctx = retrieve_context(query)
    return {"rag_context": ctx}


async def maybe_web_search(state: InterviewState) -> dict[str, Any]:
    if not state.get("use_web_search"):
        return {"web_context": ""}
    q = state.get("question_context") or state["interviewee_text"]
    result = await web_search(f"HR interview evaluation: {q[:200]}")
    return {"web_context": result}


async def score_answer(state: InterviewState) -> dict[str, Any]:
    user_block = f"""Question / topic:
{state.get('question_context') or '(not specified)'}

Interviewee said:
{state['interviewee_text']}

Reference Q&A (RAG):
{state.get('rag_context', '')}

Supplementary web context:
{state.get('web_context') or '(none)'}
"""
    response = await _llm().ainvoke(
        [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=user_block)]
    )
    text = response.content if isinstance(response.content, str) else str(response.content)
    grade: Grade = "C"
    rationale = text
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            parsed = json.loads(match.group())
            g = parsed.get("grade", "C").upper()
            if g in ("A", "B", "C", "D", "F"):
                grade = g  # type: ignore[assignment]
            rationale = parsed.get("rationale", text)
    except json.JSONDecodeError:
        for letter in ("A", "B", "C", "D", "F"):
            if f"grade\": \"{letter}" in text or f"Grade: {letter}" in text:
                grade = letter  # type: ignore[assignment]
                break

    return {
        "grade": grade,
        "rationale": rationale,
        "messages": [HumanMessage(content=user_block), response],
    }


def build_scorer_graph():
    graph = StateGraph(InterviewState)
    graph.add_node("retrieve_rag", retrieve_rag)
    graph.add_node("maybe_web_search", maybe_web_search)
    graph.add_node("score_answer", score_answer)

    graph.set_entry_point("retrieve_rag")
    graph.add_edge("retrieve_rag", "maybe_web_search")
    graph.add_edge("maybe_web_search", "score_answer")
    graph.add_edge("score_answer", END)

    return graph.compile()


scorer_graph = build_scorer_graph()


async def score_interview_turn(
    session_id: str,
    interviewee_text: str,
    question_context: str = "",
    use_web_search: bool = False,
) -> dict[str, str]:
    result = await scorer_graph.ainvoke(
        {
            "messages": [],
            "session_id": session_id,
            "question_context": question_context,
            "interviewee_text": interviewee_text,
            "rag_context": "",
            "web_context": "",
            "grade": "C",
            "rationale": "",
            "use_web_search": use_web_search,
        }
    )
    return {"grade": result["grade"], "rationale": result["rationale"]}
