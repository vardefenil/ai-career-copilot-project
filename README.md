<div align="center">

# 🤖 AI Career Copilot

### A Production-Ready RAG Agent for Resume Q&A — Locally, Privately, No API Key Needed

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-1.3-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.2-FF6B6B?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![FAISS](https://img.shields.io/badge/FAISS-1.14-4285F4?style=for-the-badge&logo=meta&logoColor=white)](https://github.com/facebookresearch/faiss)
[![Ollama](https://img.shields.io/badge/Ollama-Llama%203.1-white?style=for-the-badge)](https://ollama.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<br/>

**[🌐 Live Demo →](https://vardefenil.github.io/ai-career-copilot-project/)**&nbsp;&nbsp;|&nbsp;&nbsp;**[📖 API Docs →](http://localhost:8000/docs)**&nbsp;&nbsp;|&nbsp;&nbsp;**[👤 Author →](https://linkedin.com/in/fenil-varde-58145b318/)**

<br/>

![AI Career Copilot Demo](https://raw.githubusercontent.com/vardefenil/ai-career-copilot-project/main/assets/demo-preview.png)

</div>

---

## 🎯 What Is This?

**AI Career Copilot** is a full-stack AI application that lets anyone ask natural-language questions about a resume and get intelligent, context-aware answers — **completely locally**, with zero data sent to the cloud.

It showcases a complete **RAG (Retrieval-Augmented Generation)** pipeline — one of the most in-demand architectures in modern AI engineering — combined with a production-ready **FastAPI backend** and a stunning **glassmorphism chat frontend**.

> 💡 Ask *"What projects have you built?"* or *"What are your AI skills?"* and watch the agent search the resume using vector similarity and respond using a local LLM.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Full RAG Pipeline** | Resume → chunked → vectorized → FAISS indexed → semantic retrieval |
| 🤖 **ReAct Agent** | LangGraph-powered agent with tool use (not just a chain) |
| 🔒 **100% Private** | Everything runs locally — no OpenAI, no cloud, no API keys |
| ⚡ **FastAPI Backend** | Production REST API with Swagger docs, CORS, live/demo modes |
| 🌐 **Interactive Frontend** | Dark glassmorphism UI, typewriter animation, mobile-responsive |
| 🟢 **GitHub Pages Demo** | Static demo works without any server via pre-built Q&A engine |
| 📄 **Multi-format Ingestion** | Supports `.md`, `.txt`, and `.pdf` resume files |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI Career Copilot                        │
├──────────────────────┬──────────────────────────────────────────┤
│      FRONTEND        │              BACKEND                     │
│  frontend/index.html │          app/main.py (FastAPI)           │
│  frontend/style.css  │          app/api.py   (Chat logic)       │
│  frontend/app.js     │          app/demo_responses.py           │
│                      │                                          │
│  ┌─────────────┐     │   ┌─────────────┐  ┌─────────────────┐  │
│  │  Chat UI    │────►│──►│  /chat API  │─►│  Demo Mode      │  │
│  │ (Demo/Live) │     │   │             │  │  (pre-built)    │  │
│  └─────────────┘     │   └──────┬──────┘  └─────────────────┘  │
│                      │          │                               │
│                      │   ┌──────▼──────────────────────────┐   │
│                      │   │         AGENT PIPELINE           │   │
│                      │   │  agent/agent.py  (ReAct Agent)  │   │
│                      │   │  agent/tools.py  (FAISS Search) │   │
│                      │   └──────┬──────────────────────────┘   │
│                      │          │                               │
│                      │   ┌──────▼──────┐  ┌────────────────┐   │
│                      │   │ FAISS Index │  │ Ollama + Llama │   │
│                      │   │ (vectors)   │  │ 3.1 8B (local) │   │
│                      │   └─────────────┘  └────────────────┘   │
│                      │          ▲                               │
│                      │   ┌──────┴──────────────────────────┐   │
│                      │   │  ingestion/build_index.py        │   │
│                      │   │  Resume (.md / .pdf) → Chunks    │   │
│                      │   │  → HuggingFace Embeddings → FAISS│   │
│                      │   └─────────────────────────────────-┘   │
└──────────────────────┴──────────────────────────────────────────┘
```

### How RAG Works Here

```
Your Question
     │
     ▼
[HuggingFace Embeddings]  → converts query to a 384-dim vector
     │
     ▼
[FAISS Vector Search]     → finds top-5 most semantically similar resume chunks
     │
     ▼
[LangGraph ReAct Agent]   → reasons: "I should use search_my_background tool"
     │
     ▼
[Llama 3.1 8B via Ollama] → generates a natural language answer from retrieved context
     │
     ▼
[FastAPI /chat endpoint]  → returns JSON response to the frontend
```

---

## 🗂️ Project Structure

```
ai-career-copilot/
│
├── frontend/                    # 🌐 Web UI (GitHub Pages ready)
│   ├── index.html               #    Chat interface (glassmorphism dark)
│   ├── style.css                #    Premium CSS with animations
│   └── app.js                   #    Demo mode + Live API logic
│
├── app/                         # ⚡ FastAPI Backend
│   ├── __init__.py
│   ├── main.py                  #    API entry point + static file serving
│   ├── api.py                   #    Chat endpoint logic
│   └── demo_responses.py        #    Pre-built demo Q&A (no Ollama needed)
│
├── agent/                       # 🤖 AI Agent
│   ├── agent.py                 #    LangGraph ReAct agent (Llama 3.1 via Ollama)
│   ├── tools.py                 #    FAISS search tool
│   └── test_tools.py            #    Quick retrieval test
│
├── ingestion/
│   └── build_index.py           # 📥 Resume → FAISS vector database
│
├── data/                        # 📄 Your resume (git-ignored, private)
│   └── your_resume.md
│
├── faiss_index/                 # 🗄️ Vector DB (generated, git-ignored)
│   ├── index.faiss
│   └── index.pkl
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- Git

### 1. Clone the repository

```bash
git clone https://github.com/vardefenil/ai-career-copilot-project.git
cd ai-career-copilot-project
```

### 2. Create virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your resume

Place your resume inside `data/`:

```
data/your_resume.md    # Markdown format (recommended)
# OR
data/your_resume.pdf   # PDF also supported
```

### 5. Pull the Ollama model

```bash
ollama pull llama3.1:8b
```

---

## ▶️ Running the Project

### Step 1 — Build the vector database (run once)

```bash
python ingestion/build_index.py
```

This chunks your resume, creates embeddings, and saves the FAISS index.

### Step 2 — Start the FastAPI backend

```bash
# Make sure Ollama is running first:
ollama serve

# In a new terminal, start the API:
uvicorn app.main:app --reload --port 8000
```

Visit **http://localhost:8000** to see the full UI, or **http://localhost:8000/docs** for the Swagger API explorer.

### Step 3 — Open the frontend (alternative)

Open `frontend/index.html` directly in your browser for the demo mode (no backend needed).

Or visit the **[Live Demo →](https://vardefenil.github.io/ai-career-copilot-project/)**

### CLI mode (original)

```bash
python -m agent.agent
```

---

## 🌐 Live Demo

The live demo is hosted on **GitHub Pages** and uses a smart demo mode — pre-built answers based on Fenil's resume — so you can interact with it without needing Ollama or any server.

**[→ Try the Live Demo](https://vardefenil.github.io/ai-career-copilot-project/)**

| Mode | Requires | Use when |
|------|----------|----------|
| 🟢 Demo Mode | Nothing | GitHub Pages, sharing, quick preview |
| ⚡ Live Mode | Ollama + FAISS index | Full local experience with your own resume |

---

## 🔌 API Reference

### `POST /chat`

```json
// Request
{
  "query": "What projects has Fenil built?",
  "demo": true
}

// Response
{
  "answer": "🚀 Here are Fenil's key projects: ...",
  "mode": "demo",
  "processing_time_ms": 142
}
```

Set `demo: false` to use the real Ollama agent.

### `GET /health`

```json
{ "status": "ok", "service": "AI Career Copilot" }
```

Full interactive API docs: **http://localhost:8000/docs**

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML · CSS · Vanilla JS | Premium glassmorphism chat UI |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com) + Uvicorn | REST API, CORS, static serving |
| **Agent** | [LangGraph](https://langchain-ai.github.io/langgraph/) | ReAct agent loop with tool use |
| **LLM** | [Ollama](https://ollama.com) + Llama 3.1 8B | Local inference, zero cloud cost |
| **Retrieval** | [FAISS](https://github.com/facebookresearch/faiss) | Vector similarity search |
| **Embeddings** | [HuggingFace](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) all-MiniLM-L6-v2 | Text → 384-dim vectors |
| **Framework** | [LangChain](https://langchain.com) | Tool orchestration & chains |
| **Ingestion** | PyPDF + LangChain Splitters | PDF/MD → chunks |

---

## 💬 Example Interactions

```
You: What projects has Fenil built?

🤖 AI Career Copilot:
1. AI Career Copilot (2026)
   → RAG-based AI agent, FAISS + LangGraph + Ollama. Zero cloud dependency.

2. Credit Card Fraud Detection System (2026)
   → Logistic Regression, Random Forest, SVM, XGBoost on imbalanced data.
   → Flask dashboard for real-time predictions.

3. AI-Based Resume Analytics Tool (2026)
   → PDF parsing, 10+ extracted fields, ~60% reduction in manual review.

4. AI-Powered Voice Assistant (2024)
   → Google Gemini AI, 20+ voice commands, NewsAPI, music playback.
```

---

## 🔒 Privacy First

Your resume **never leaves your machine**:

- ✅ **Embeddings** — local HuggingFace model (`all-MiniLM-L6-v2`)
- ✅ **LLM** — Ollama runs 100% locally (Llama 3.1 8B)
- ✅ **Vector DB** — FAISS files stored on your disk
- ✅ **No API keys** — no OpenAI, Anthropic, or any cloud LLM

---

## 👤 Author

**Fenil Varde** — Computer Engineering undergraduate building AI systems that matter.

[![GitHub](https://img.shields.io/badge/GitHub-vardefenil-181717?style=flat-square&logo=github)](https://github.com/vardefenil)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Fenil%20Varde-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/fenil-varde-58145b318/)
[![LeetCode](https://img.shields.io/badge/LeetCode-vardefenil6-FFA116?style=flat-square&logo=leetcode&logoColor=black)](https://leetcode.com/u/vardefenil6/)
[![Email](https://img.shields.io/badge/Email-vardefenil6%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:vardefenil6@gmail.com)

---

## 📄 License

MIT © 2026 Fenil Varde

---

<div align="center">

**⭐ If you found this useful, please star the repo!**

*Built with ❤️ using Python, LangChain, and a deep interest in practical AI engineering.*

</div>
