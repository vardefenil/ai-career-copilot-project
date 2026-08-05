# 🤖 AI Career Copilot

A **RAG (Retrieval-Augmented Generation)** AI agent that answers questions about your resume — locally, privately, with no API key needed.

Ask it *"List all my projects"* or *"What are my skills?"* and it searches your resume using vector similarity and answers using a local LLM.

---

## 🧠 How It Works

```
Your Resume (.md / .pdf)
        ↓
  ingestion/build_index.py   → splits resume into chunks → converts to vectors → saves to faiss_index/
        ↓
  agent/tools.py             → loads vectors → exposes search_my_background() tool
        ↓
  agent/agent.py             → ReAct AI agent (Llama 3.1 via Ollama) uses the tool to answer questions
```

---

## 🗂️ Project Structure

```
ai-career-copilot/
│
├── data/                        # Your resume (not committed — private)
│   └── fenil_resume.md
│
├── faiss_index/                 # Vector database (generated — not committed)
│   ├── index.faiss
│   └── index.pkl
│
├── ingestion/
│   └── build_index.py           # Step 1: Build vector DB from resume
│
├── agent/
│   ├── __init__.py
│   ├── tools.py                 # Step 2: Search tool using FAISS
│   ├── test_tools.py            # Quick retrieval test (no LLM)
│   └── agent.py                 # Step 3: Full AI agent
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed and running

### 1. Clone the repo
```bash
git clone https://github.com/vardefenil/ai-career-cpilot-project.git
cd ai-career-cpilot-project
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your resume
Place your resume as a markdown or text file inside `data/`:
```
data/your_resume.md
```
Update the filename in `ingestion/build_index.py` line 10 if needed.

### 5. Pull the Ollama model
```bash
ollama pull llama3.1:8b
```

---

## ▶️ Running the Project

### Step 1 — Build the vector database (once)
```bash
python ingestion/build_index.py
```

### Step 2 — Test retrieval (no LLM needed)
```bash
python -m agent.test_tools
```

### Step 3 — Run the full AI agent
```bash
# Make sure Ollama is running first:
ollama serve

# Then in another terminal:
python -m agent.agent
```

---

## 💬 Example Output

```
Querying agent: 'List all the projects mentioned in my resume.'

--- Agent Response ---
1. Credit Card Fraud Detection System
   → Python, scikit-learn, Pandas
   → Built fraud detection using Logistic Regression, Random Forest, SVM, XGBoost

2. AI-Based Resume Analytics Tool
   → Python, Flask, NLP, scikit-learn
   → Parses PDFs, extracts 10+ structured fields

3. AI-Powered Voice Assistant
   → Python, Gemini AI, NewsAPI
   → 20+ voice commands, real-time news, music playback
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [LangChain](https://langchain.com) | Agent framework & tool orchestration |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | ReAct agent loop |
| [FAISS](https://github.com/facebookresearch/faiss) | Vector similarity search |
| [HuggingFace Sentence Transformers](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | Text → vector embeddings |
| [Ollama](https://ollama.com) + Llama 3.1 8B | Local LLM (no API key needed) |

---

## 🔒 Privacy

Your resume **never leaves your machine**. Everything runs 100% locally:
- Embeddings: local HuggingFace model
- LLM: Ollama (local)
- Vector DB: local FAISS files

---

## 📄 License

MIT
