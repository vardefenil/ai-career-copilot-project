"""
Demo responses for GitHub Pages live demo.
These are pre-built answers based on Fenil Varde's resume,
so visitors can interact with the AI without needing a running backend.
"""

DEMO_QA = {
    "projects": {
        "keywords": ["project", "projects", "built", "created", "work", "portfolio", "apps", "applications"],
        "answer": (
            "🚀 Here are my key projects:\n\n"
            "**1. AI Career Copilot** (2026)\n"
            "→ RAG-based AI agent that answers questions about a resume locally using FAISS + LangGraph + Ollama (Llama 3.1 8B). No API key needed.\n\n"
            "**2. Credit Card Fraud Detection System** (2026)\n"
            "→ End-to-end fraud detection using Logistic Regression, Random Forest, SVM & XGBoost on imbalanced datasets. Built a Flask dashboard for real-time predictions.\n\n"
            "**3. AI-Based Resume Analytics Tool** (2026)\n"
            "→ Parses PDF resumes and extracts 10+ structured fields (skills, education, experience) using Python, Flask & NLP. Reduced manual review effort by ~60%.\n\n"
            "**4. AI-Powered Voice Assistant** (2024)\n"
            "→ Voice-controlled desktop assistant with 20+ command types. Integrates Google Gemini AI, NewsAPI, music playback & website navigation."
        ),
    },
    "skills": {
        "keywords": ["skill", "skills", "tech", "technology", "know", "language", "languages", "tools", "stack", "expertise"],
        "answer": (
            "🛠️ My Technical Skills:\n\n"
            "**Languages:** Python · C++ · HTML · CSS\n\n"
            "**AI / ML:** LangChain · LangGraph · FAISS · scikit-learn · Transformers · RAG · ReAct Agents\n\n"
            "**ML Libraries:** NumPy · Pandas · Matplotlib · Seaborn · HuggingFace\n\n"
            "**Web / Backend:** Flask · FastAPI · REST APIs\n\n"
            "**Tools:** Git · GitHub · VS Code · Jupyter Notebook · Ollama\n\n"
            "**Concepts:** Feature Engineering · Model Evaluation · Cross Validation · Imbalanced Data Handling · Vector Embeddings"
        ),
    },
    "education": {
        "keywords": ["education", "college", "university", "degree", "study", "studied", "school", "gpa", "cpi", "grade", "academic"],
        "answer": (
            "🎓 My Education:\n\n"
            "**B.E. in Computer Engineering** (2023 – 2027)\n"
            "LDRP Institute of Technology and Research, Gandhinagar, Gujarat\n"
            "CPI: 7.66 / 10.00\n\n"
            "**Relevant Coursework:**\n"
            "Data Structures · Object-Oriented Programming · Database Management Systems · Operating Systems\n\n"
            "**Higher Secondary (Class XII):** GSEB Science — 56.92%\n"
            "**Secondary School (Class X):** GSEB — 80.83%"
        ),
    },
    "experience": {
        "keywords": ["experience", "work", "job", "internship", "company", "role", "position", "employed"],
        "answer": (
            "💼 Experience & Background:\n\n"
            "I am currently a **3rd-year Computer Engineering student** at LDRP Institute of Technology and Research (2023–2027).\n\n"
            "While I don't have formal industry experience yet, I have built multiple end-to-end AI/ML projects independently, including:\n"
            "• A RAG-based AI career assistant (this project!)\n"
            "• A fraud detection system with a Flask dashboard\n"
            "• An AI-powered voice assistant using Google Gemini\n\n"
            "I am actively seeking **internship opportunities** in AI/ML and Python development."
        ),
    },
    "certifications": {
        "keywords": ["certif", "certificate", "certification", "course", "nptel", "achievement", "award", "medal"],
        "answer": (
            "🏅 Certifications & Achievements:\n\n"
            "**Certifications:**\n"
            "• NPTEL — Programming in Python (IIT Madras) — Elite Badge (2024)\n\n"
            "**Achievements:**\n"
            "• JEE Main 2023 — 87.38 Percentile overall, 85.42 Percentile in Mathematics (among 1M+ candidates)\n"
            "• 🥈 Silver Medalist — District Level Judo Competition\n"
            "• Actively solving DSA problems on LeetCode & Codeforces"
        ),
    },
    "contact": {
        "keywords": ["contact", "email", "phone", "linkedin", "github", "reach", "hire", "connect", "social"],
        "answer": (
            "📬 Get in touch with Fenil:\n\n"
            "📧 **Email:** vardefenil6@gmail.com\n"
            "📱 **Phone:** +91 87804 71545\n"
            "💼 **LinkedIn:** [fenil-varde-58145b318](https://www.linkedin.com/in/fenil-varde-58145b318/)\n"
            "🐙 **GitHub:** [vardefenil](https://github.com/vardefenil)\n"
            "⚡ **LeetCode:** [vardefenil6](https://leetcode.com/u/vardefenil6/)\n\n"
            "Feel free to reach out for collaborations, internship opportunities, or just to connect!"
        ),
    },
    "default": {
        "answer": (
            "👋 Hi! I'm Fenil's AI Career Copilot.\n\n"
            "I can answer questions about:\n"
            "• 🚀 **Projects** — What I've built\n"
            "• 🛠️ **Skills** — Technologies I know\n"
            "• 🎓 **Education** — My academic background\n"
            "• 🏅 **Achievements** — Certifications & awards\n"
            "• 📬 **Contact** — How to reach Fenil\n\n"
            "Try asking: *\"What projects have you built?\"* or *\"What are your skills?\"*"
        ),
    },
}


def get_demo_response(query: str) -> str:
    """
    Match a user query to the best pre-built demo response.
    Falls back to the default greeting if no match is found.
    """
    query_lower = query.lower()

    for category, data in DEMO_QA.items():
        if category == "default":
            continue
        if any(kw in query_lower for kw in data["keywords"]):
            return data["answer"]

    return DEMO_QA["default"]["answer"]
