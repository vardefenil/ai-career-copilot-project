"""
API endpoint logic for AI Career Copilot.
Handles both LIVE mode (uses the real LangGraph agent) and DEMO mode (uses pre-built responses).
"""

import time
from typing import Generator

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.demo_responses import get_demo_response


# ── Request / Response schemas ─────────────────────────────────────────────
class ChatRequest(BaseModel):
    query: str
    demo: bool = False  # If True, use pre-built demo responses (no Ollama needed)


class ChatResponse(BaseModel):
    answer: str
    mode: str  # "live" or "demo"
    processing_time_ms: int


# ── Lazy-load the real agent (only when LIVE mode is requested) ────────────
_agent = None


def _get_agent():
    """Load the LangGraph agent lazily to avoid import errors if Ollama is not running."""
    global _agent
    if _agent is None:
        try:
            from agent.agent import agent  # noqa: PLC0415
            _agent = agent
        except Exception as exc:
            raise HTTPException(
                status_code=503,
                detail=(
                    f"Agent failed to load: {exc}. "
                    "Make sure Ollama is running (`ollama serve`) and the model is pulled (`ollama pull llama3.1:8b`). "
                    "Use ?demo=true for a demo without Ollama."
                ),
            ) from exc
    return _agent


# ── Helpers ────────────────────────────────────────────────────────────────
def _run_live_agent(query: str) -> str:
    """Run the real LangGraph ReAct agent and return its response."""
    from langchain_core.messages import HumanMessage  # noqa: PLC0415

    agent = _get_agent()
    response = agent.invoke({"messages": [HumanMessage(content=query)]})
    final_msg = response["messages"][-1]
    return final_msg.content.encode("utf-8", errors="replace").decode("utf-8")


# ── Chat handler ───────────────────────────────────────────────────────────
def handle_chat(request: ChatRequest) -> ChatResponse:
    """
    Main chat handler.
    - demo=True  → returns pre-built answer instantly
    - demo=False → invokes real LangGraph agent (requires Ollama)
    """
    start = time.time()

    if request.demo:
        answer = get_demo_response(request.query)
        mode = "demo"
    else:
        answer = _run_live_agent(request.query)
        mode = "live"

    elapsed_ms = int((time.time() - start) * 1000)
    return ChatResponse(answer=answer, mode=mode, processing_time_ms=elapsed_ms)
