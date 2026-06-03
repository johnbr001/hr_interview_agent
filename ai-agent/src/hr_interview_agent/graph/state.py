from typing import Annotated, Literal, TypedDict

from langgraph.graph.message import add_messages


Grade = Literal["A", "B", "C", "D", "F"]


class InterviewState(TypedDict):
    messages: Annotated[list, add_messages]
    session_id: str
    question_context: str
    interviewee_text: str
    rag_context: str
    web_context: str
    grade: Grade
    rationale: str
    use_web_search: bool
