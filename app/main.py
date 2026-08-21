"""
AI Career Copilot — FastAPI Application Entry Point

Usage:
    uvicorn app.main:app --reload --port 8000
    Open: http://localhost:8000

Endpoints:
    GET  /              — Chat UI frontend
    GET  /style.css     — CSS
    GET  /app.js        — JavaScript
    POST /chat          — Chat with the AI agent
    GET  /health        — Health check
    GET  /docs          — Swagger UI
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from app.api import ChatRequest, ChatResponse, handle_chat

# Load .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# ── Paths ──────────────────────────────────────────────────────────────────
_ROOT_DIR     = os.path.dirname(os.path.dirname(__file__))
_FRONTEND_DIR = os.path.join(_ROOT_DIR, "frontend")

# ── App ────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="AI Career Copilot API",
    description="RAG-powered AI agent for Fenil Varde's resume. Built with LangChain · LangGraph · FAISS · Gemini · FastAPI.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ───────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Static asset routes ────────────────────────────────────────────────────
@app.get("/style.css", include_in_schema=False)
async def serve_css():
    return FileResponse(os.path.join(_FRONTEND_DIR, "style.css"), media_type="text/css")


@app.get("/app.js", include_in_schema=False)
async def serve_js():
    return FileResponse(os.path.join(_FRONTEND_DIR, "app.js"), media_type="application/javascript")


# ── Root → Chat UI ─────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    index_path = os.path.join(_FRONTEND_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path, media_type="text/html")
    return JSONResponse({"error": "Frontend not found."}, status_code=404)


# ── API Routes ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["Info"])
async def health():
    """Health check."""
    gemini_key_set = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    return {
        "status": "ok",
        "service": "AI Career Copilot",
        "version": "2.0.0",
        "gemini_configured": gemini_key_set,
        "mode": "live" if gemini_key_set else "demo-fallback",
    }


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with the AI Career Copilot.
    - **query**: Your question about Fenil's resume  
    - **demo**: Set `true` for instant pre-built answers (no API key needed)
    """
    return handle_chat(request)
