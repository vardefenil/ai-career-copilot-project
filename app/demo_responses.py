"""
Demo responses for GitHub Pages live demo.
These are pre-built answers based on Fenil Varde's resume,
so visitors can interact with the AI without needing a running backend.
"""

DEMO_QA = {
    "ats": {
        "keywords": ["ats", "score", "audit", "resume review", "review resume", "format", "keyword"],
        "answer": (
            "📊 **Comprehensive ATS Resume Scan & Score**\n\n"
            "### 🎯 Estimated ATS Score: **88 / 100** (Grade: Strong Candidate)\n\n"
            "---\n\n"
            "### ✅ Key Strengths:\n"
            "• **Quantifiable Metrics:** Clear impact points (e.g. *\"reducing manual review by 60%\"*, *\"20+ voice command types\"*, *\"10+ structured fields\"*).\n"
            "• **Clean Tech Stacks:** Distinct technologies listed per project (Python, scikit-learn, LangChain, FAISS, Flask).\n"
            "• **Standard Headings:** Follows universal ATS section conventions (*Summary, Education, Projects, Technical Skills, Certifications*).\n\n"
            "### 🔍 Recommended Keywords for AI/ML Roles:\n"
            "• Add: `FastAPI`, `Vector Databases`, `RAG (Retrieval-Augmented Generation)`, `Prompt Engineering`, `Docker`, `CI/CD`.\n\n"
            "### 🚀 Action Verb Enhancement:\n"
            "• *Before:* 'Built an end-to-end fraud detection system...'\n"
            "• *After:* 'Architected & deployed a production ML fraud detection pipeline across 4 classifier models with 94%+ ROC-AUC.'"
        ),
    },
    "job_match": {
        "keywords": ["job match", "match", "jd", "job description", "fit", "qualif", "requirements"],
        "answer": (
            "💼 **Job Description Match Analysis**\n\n"
            "### 🎯 Match Score: **85% Alignment for AI/ML & Python Developer Roles**\n\n"
            "---\n\n"
            "### 🟢 Exact Matches Found:\n"
            "• **Languages & Frameworks:** Python, C++, scikit-learn, Pandas, NumPy, Flask, FastAPI.\n"
            "• **AI / Architecture:** RAG Pipelines, Vector Search (FAISS), ReAct Agents (LangGraph), LLM APIs (Gemini).\n"
            "• **Core CS:** Data Structures & Algorithms, OOP, Database Management (SQL).\n\n"
            "### 🟡 Recommendations / Next Steps:\n"
            "• Emphasize containerization (Docker) and Cloud deployment (AWS/GCP).\n"
            "• Highlight the end-to-end RAG workflow built in the AI Career Copilot project during technical rounds."
        ),
    },
    "interview": {
        "keywords": ["interview", "mock", "question", "questions", "prepare", "prep", "behavioral", "technical round"],
        "answer": (
            "🎙️ **Tailored Technical & Behavioral Mock Interview**\n\n"
            "### 1. Technical Project Deep-Dive (Credit Card Fraud Detection):\n"
            "**Q:** *\"How did you handle the class imbalance in your fraud detection dataset, and why choose Precision-Recall / ROC-AUC over Accuracy?\"*\n"
            "👉 **Key talking points:** Mention techniques like SMOTE, class weighting in Random Forest / XGBoost, and how accuracy is deceptive in 99:1 imbalanced transaction data.\n\n"
            "### 2. Architecture & RAG (AI Career Copilot):\n"
            "**Q:** *\"Explain how chunk size and overlap in RecursiveCharacterTextSplitter impact retrieval accuracy in FAISS.\"*\n"
            "👉 **Key talking points:** Discuss context preservation across chunk boundaries (e.g. 1000 chars with 200 overlap) and avoiding hallucination in LLM prompts.\n\n"
            "### 3. Behavioral (STAR Method):\n"
            "**Q:** *\"Tell me about a challenging bug you encountered while integrating Gemini AI in your voice assistant and how you resolved it.\"*"
        ),
    },
    "cold_email": {
        "keywords": ["cold email", "email", "cover letter", "outreach", "recruiter", "hiring manager", "message"],
        "answer": (
            "✉️ **Tailored Recruiter Outreach & Cover Letter**\n\n"
            "### 📬 High-Conversion Cold Email:\n\n"
            "**Subject:** B.E. Computer Engineering Student | Applied AI & RAG Developer — Fenil Varde\n\n"
            "Hi [Hiring Manager / Recruiter Name],\n\n"
            "I've been following [Company Name]'s recent work in AI engineering. As a Computer Engineering undergraduate with hands-on experience building end-to-end RAG systems (LangGraph + FAISS + Gemini) and production ML pipelines (Fraud Detection with XGBoost), I would love to contribute to your engineering team.\n\n"
            "A quick look at my work:\n"
            "• **AI Career Copilot:** Live RAG agent querying complex unstructured documents with sub-second retrieval.\n"
            "• **Fraud Detection System:** Evaluated 4 ML algorithms on imbalanced data with real-time Flask analytics.\n\n"
            "Are you open to a brief 10-minute chat this week?\n\n"
            "Best regards,\n"
            "**Fenil Varde**\n"
            "🔗 LinkedIn: linkedin.com/in/fenil-varde-58145b318/ | 🐙 GitHub: github.com/vardefenil"
        ),
    },
    "projects": {
        "keywords": ["project", "projects", "built", "created", "work", "portfolio", "apps", "applications"],
        "answer": (
            "🚀 Here are Fenil's key projects:\n\n"
            "**1. AI Career Copilot** (2026)\n"
            "→ RAG-based AI agent that answers questions about a resume locally using FAISS + LangGraph + Google Gemini 3.6 Flash. Features live PDF upload, ATS scoring, and interview prep.\n\n"
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
            "**AI / ML:** LangChain · LangGraph · FAISS · scikit-learn · Transformers · RAG · ReAct Agents · Google Gemini\n\n"
            "**ML Libraries:** NumPy · Pandas · Matplotlib · Seaborn · HuggingFace\n\n"
            "**Web / Backend:** FastAPI · Flask · REST APIs\n\n"
            "**Tools:** Git · GitHub · VS Code · Jupyter Notebook\n\n"
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
            "• 📊 **ATS Score** — Check resume ATS compatibility\n"
            "• 💼 **Job Match** — Compare against a job description\n"
            "• 🎙️ **Mock Interview** — Practice technical & STAR questions\n"
            "• ✉️ **Outreach** — Generate cold email & cover letter\n"
            "• 🎓 **Education & Certifications**\n\n"
            "Try clicking one of the quick tools in the sidebar or ask anything!"
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
