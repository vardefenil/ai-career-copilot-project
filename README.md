<div align="center">

# 🤖 AI Career Copilot

### Full-Stack RAG AI Agent for Resume Q&A, ATS Scoring, Job Matching, & Mock Interviews

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-3.6%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.2-FF6B6B?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![FAISS](https://img.shields.io/badge/FAISS-1.14-4285F4?style=for-the-badge&logo=meta&logoColor=white)](https://github.com/facebookresearch/faiss)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<br/>

**[🌐 Live Demo →](https://vardefenil.github.io/ai-career-copilot-project/frontend/index.html)**&nbsp;&nbsp;|&nbsp;&nbsp;**[📖 API Docs →](http://localhost:8000/docs)**&nbsp;&nbsp;|&nbsp;&nbsp;**[👤 Author →](https://linkedin.com/in/fenil-varde-58145b318/)**

<br/>

![AI Career Copilot Demo](https://raw.githubusercontent.com/vardefenil/ai-career-copilot-project/main/assets/demo-preview.png)

</div>

---

## 🎯 What Is This?

**AI Career Copilot** is a production-grade, full-stack AI career platform powered by **Retrieval-Augmented Generation (RAG)**, **LangGraph ReAct Agents**, and **Google Gemini 3.6 Flash**.

Upload any resume (`.pdf`, `.md`, `.txt`) or interact with the pre-indexed profile to:
- 💬 **Ask anything** about projects, skills, education, and technical architectures.
- 📊 **Run an ATS Audit** with estimated scores (0-100), missing keywords, and impact enhancements.
- 💼 **Match Job Descriptions (JD)** to calculate % alignment and generate custom talking points.
- 🎙️ **Practice Mock Interviews** with tailored technical deep-dives and STAR frameworks.
- ✉️ **Generate Recruiter Outreach** & customized cover letters with 1-click copy.

---

## ✨ Specialized Agent Tools

| Tool | Capability |
| :--- | :--- |
| 🔍 **`search_my_background`** | Semantic RAG vector search across all resume chunks using FAISS. |
| 📊 **`analyze_resume_ats`** | Comprehensive ATS scan, keyword gap analysis, and bullet point upgrades. |
| 💼 **`match_job_description`** | Multi-dimensional candidate-to-job matching & positioning strategy. |
| 🎙️ **`generate_mock_interview`** | Role-specific technical & behavioral interview simulations. |
| ✉️ **`create_cold_email_cover_letter`** | High-conversion outreach emails and customized cover letters. |

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AI Career Copilot                               │
├───────────────────────┬────────────────────────────────────────────────┤
│       FRONTEND        │                    BACKEND                     │
│  frontend/index.html  │              app/main.py (FastAPI)             │
│  frontend/style.css   │              app/api.py   (Agent Router)       │
│  frontend/app.js      │              app/demo_responses.py             │
│                       │                                                │
│  ┌────────────────┐   │   ┌───────────────┐     ┌──────────────────┐   │
│  │ Chat & Tool UI │───┼──►│ /chat API     │────►│ Google Gemini    │   │
│  └────────────────┘   │   └───────┬───────┘     │ 3.6 Flash        │   │
│                       │           │             └────────┬─────────┘   │
│  ┌────────────────┐   │   ┌───────▼───────┐              │             │
│  │ PDF Upload     │───┼──►│/upload-resume │              │             │
│  └────────────────┘   │   └───────┬───────┘              │             │
│                       │           │                      │             │
│                       │   ┌───────▼──────────────────────▼─────────┐   │
│                       │   │            LANGGRAPH REACT AGENT       │   │
│                       │   │ 5 Tools: search_bg, ats_scan, jd_match,│   │
│                       │   │          mock_interview, cold_outreach │   │
│                       │   └──────────────────────┬─────────────────┘   │
│                       │                          │                     │
│                       │                 ┌────────▼────────┐            │
│                       │                 │   FAISS Vector  │            │
│                       │                 │   Database      │            │
│                       │                 └─────────────────┘            │
└───────────────────────┴────────────────────────────────────────────────┘
```

---

## ⚙️ Quickstart & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/vardefenil/ai-career-copilot-project.git
cd ai-career-copilot-project
```

### 2. Set up virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS / Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API Key
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=AIzaSy...your_gemini_api_key
```
*(Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey))*

### 5. Build vector index & Launch!
```bash
# Build FAISS index from data/ folder:
python ingestion/build_index.py

# Launch FastAPI web app:
uvicorn app.main:app --reload --port 8000
```
Open **http://localhost:8000** in your browser!

---

## 🔌 API Endpoints

- **`POST /chat`**: Query the AI Career Copilot agent.
- **`POST /upload-resume`**: Upload any `.pdf` resume to re-index live in real-time.
- **`GET /health`**: Status check and list of indexed documents.
- **`GET /docs`**: Interactive Swagger API Explorer.

---

## 👤 Author

**Fenil Varde** — Computer Engineering Undergraduate & Applied AI Developer
- 💼 **LinkedIn:** [fenil-varde-58145b318](https://linkedin.com/in/fenil-varde-58145b318/)
- 🐙 **GitHub:** [vardefenil](https://github.com/vardefenil)
- ⚡ **LeetCode:** [vardefenil6](https://leetcode.com/u/vardefenil6/)

---

## 📄 License
MIT © 2026 Fenil Varde
