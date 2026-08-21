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
    POST /upload-resume — Upload a new PDF resume & live re-index
    GET  /health        — Health check
    GET  /docs          — Swagger UI
"""

import os
import shutil
import glob

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from app.api import ChatRequest, ChatResponse, handle_chat
from agent.tools import reload_vectorstore
from ingestion.build_index import build_vector_index

# Load .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# ── Paths ──────────────────────────────────────────────────────────────────
_ROOT_DIR     = os.path.dirname(os.path.dirname(__file__))
_FRONTEND_DIR = os.path.join(_ROOT_DIR, "frontend")
_DATA_DIR     = os.path.join(_ROOT_DIR, "data")
os.makedirs(_DATA_DIR, exist_ok=True)

# ── App ────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="AI Career Copilot API",
    description="RAG-powered AI agent for Resume Q&A, ATS scoring, Job Matching, & Mock Interviews. Built with LangChain · LangGraph · FAISS · Gemini 3.6 Flash · FastAPI.",
    version="2.1.0",
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
    indexed_files = [os.path.basename(f) for f in glob.glob(os.path.join(_DATA_DIR, "*.*")) if not f.endswith(".lnk")]
    return {
        "status": "ok",
        "service": "AI Career Copilot",
        "version": "2.1.0",
        "model": "Gemini 3.6 Flash",
        "gemini_configured": gemini_key_set,
        "mode": "live" if gemini_key_set else "demo-fallback",
        "indexed_documents": indexed_files,
    }


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with the AI Career Copilot.
    - **query**: Your question about resume, ATS scoring, Job Matching, or Interviews.
    - **demo**: Set `true` for instant pre-built answers (no API key needed).
    """
    return handle_chat(request)


@app.post("/upload-resume", tags=["Resume"])
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a new resume (.pdf, .md, or .txt).
    Automatically saves the file, re-indexes it using FAISS vectorstore, and reloads the active AI agent.
    """
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".md") or file.filename.endswith(".txt")):
        raise HTTPException(status_code=400, detail="Only .pdf, .md, or .txt files are supported.")

    file_path = os.path.join(_DATA_DIR, file.filename)

    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Trigger vector index rebuild
        chunks_count, doc_count = build_vector_index(_DATA_DIR)

        # Reload live agent's vector store in-memory
        reload_vectorstore()

        return {
            "status": "success",
            "message": f"Successfully uploaded and indexed '{file.filename}'!",
            "chunks_indexed": chunks_count,
            "total_documents": doc_count,
            "filename": file.filename,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index uploaded document: {str(e)}")
