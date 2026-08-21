"""
API endpoint logic for AI Career Copilot.
Handles both LIVE mode (uses the real LangGraph agent + Gemini) and DEMO mode (pre-built responses).

Auto-fallback: if GEMINI_API_KEY is missing, live-mode calls automatically fall back to demo mode.
"""

import os
import time

from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic import BaseModel

# Load .env from project root
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

from app.demo_responses import get_demo_response


# ── Request / Response schemas ─────────────────────────────────────────────
class ChatRequest(BaseModel):
    query: str
    demo: bool = False  # If True, use pre-built demo responses (no API key needed)


class ChatResponse(BaseModel):
    answer: str
    mode: str            # "live", "demo", or "demo-fallback"
    processing_time_ms: int


# ── Check if Gemini key is available ──────────────────────────────────────
def _has_gemini_key() -> bool:
    return bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))


# ── Lazy-load the real agent (only when LIVE mode is requested) ────────────
_agent = None


def _get_agent():
    """Load the LangGraph + Gemini agent lazily."""
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
                    "Make sure GEMINI_API_KEY is set in your .env file. "
                    "Use demo=true for instant responses without an API key."
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
    - demo=True         → pre-built answer instantly (no API key needed)
    - demo=False + key  → real Gemini + FAISS agent
    - demo=False + no key → auto-falls back to demo mode with a notice
    """
    start = time.time()

    if request.demo:
        answer = get_demo_response(request.query)
        mode = "demo"

    elif not _has_gemini_key():
        # No API key — auto-fall back gracefully
        answer = (
            get_demo_response(request.query)
            + "\n\n---\n⚠️ *Running in demo mode — add GEMINI_API_KEY to .env for live AI responses.*"
        )
        mode = "demo-fallback"

    else:
        answer = _run_live_agent(request.query)
        mode = "live"

    elapsed_ms = int((time.time() - start) * 1000)
    return ChatResponse(answer=answer, mode=mode, processing_time_ms=elapsed_ms)
