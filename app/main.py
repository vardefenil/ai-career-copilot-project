"""
AI Career Copilot — FastAPI Application Entry Point

Runs the chat API that powers the frontend.

Usage:
    uvicorn app.main:app --reload --port 8000

Endpoints:
    POST /chat          — Chat with the AI agent
    GET  /health        — Health check
    GET  /              — API info
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.api import ChatRequest, ChatResponse, handle_chat

# ── App setup ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="AI Career Copilot API",
    description=(
        "A RAG-powered AI agent that answers questions about Fenil Varde's resume. "
        "Built with LangChain · LangGraph · FAISS · Ollama (Llama 3.1 8B)."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS (allows frontend to call the API from any origin) ─────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Serve frontend static files ────────────────────────────────────────────
_FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.isdir(_FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=_FRONTEND_DIR), name="static")


# ── Routes ─────────────────────────────────────────────────────────────────
@app.get("/", tags=["Info"])
async def root():
    """Serve the frontend index page or return API info."""
    index_path = os.path.join(_FRONTEND_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return {
        "name": "AI Career Copilot API",
        "version": "1.0.0",
        "description": "RAG-based AI agent for resume Q&A",
        "endpoints": {
            "POST /chat": "Chat with the AI agent",
            "GET /health": "Health check",
            "GET /docs": "Swagger UI",
        },
        "tip": "Add ?demo=true to /chat for a demo without Ollama.",
    }


@app.get("/health", tags=["Info"])
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "AI Career Copilot"}


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with the AI Career Copilot.

    - **query**: Your question about the resume
    - **demo**: If `true`, uses pre-built demo responses (no Ollama required)
    """
    return handle_chat(request)
