"""
API endpoint logic for AI Career Copilot.
Handles both LIVE mode (uses the real LangGraph agent + Gemini with thread_id memory) and DEMO mode.
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
    thread_id: str = "default"  # Unique conversation session ID
    demo: bool = False          # If True, use pre-built demo responses (no API key needed)


class ChatResponse(BaseModel):
    answer: str
    thread_id: str
    mode: str                   # "live", "demo", or "demo-fallback"
    processing_time_ms: int


# ── Check if Gemini key is available ──────────────────────────────────────
def _has_gemini_key() -> bool:
    return bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))


# ── Lazy-load the query_agent function ─────────────────────────────────────
_query_agent_func = None


def _get_query_agent():
    """Load the LangGraph agent query function lazily."""
    global _query_agent_func
    if _query_agent_func is None:
        try:
            from agent.agent import query_agent  # noqa: PLC0415
            _query_agent_func = query_agent
        except Exception as exc:
            raise HTTPException(
                status_code=503,
                detail=(
                    f"Agent failed to load: {exc}. "
                    "Make sure GEMINI_API_KEY is set in your .env file."
                ),
            ) from exc
    return _query_agent_func


# ── Chat handler ───────────────────────────────────────────────────────────
def handle_chat(request: ChatRequest) -> ChatResponse:
    """
    Main chat handler with thread_id session support.
    - demo=True         → pre-built answer instantly (no API key needed)
    - demo=False + key  → real Gemini + FAISS agent with thread memory
    - demo=False + no key → auto-falls back to demo mode with a notice
    """
    start = time.time()
    thread_id = request.thread_id or "default"

    if request.demo:
        answer = get_demo_response(request.query)
        mode = "demo"

    elif not _has_gemini_key():
        answer = (
            get_demo_response(request.query)
            + "\n\n---\n⚠️ *Running in demo mode — add GEMINI_API_KEY to .env for live AI responses.*"
        )
        mode = "demo-fallback"

    else:
        try:
            query_fn = _get_query_agent()
            answer = query_fn(request.query, thread_id=thread_id)
            mode = "live"
        except Exception as e:
            answer = f"⚠️ Error querying agent: {str(e)}"
            mode = "error"

    elapsed_ms = int((time.time() - start) * 1000)
    return ChatResponse(
        answer=answer,
        thread_id=thread_id,
        mode=mode,
        processing_time_ms=elapsed_ms,
    )
