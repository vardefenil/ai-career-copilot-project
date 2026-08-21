import io
import os
import sys
import warnings

# Suppress langchain-community deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.tools import tool

# Fix Windows console encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Base directory paths
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_FAISS_PATH = os.path.join(_BASE_DIR, "faiss_index")

# Embeddings model loaded once
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Global vectorstore
vectorstore = None

def get_vectorstore():
    """Load or retrieve the active FAISS vectorstore."""
    global vectorstore
    if vectorstore is None and os.path.exists(_FAISS_PATH):
        vectorstore = FAISS.load_local(_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    return vectorstore

def reload_vectorstore():
    """Force reload the FAISS vectorstore from disk (after new PDF upload)."""
    global vectorstore
    if os.path.exists(_FAISS_PATH):
        vectorstore = FAISS.load_local(_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    return vectorstore

# Initialize on import if index exists
get_vectorstore()


@tool
def search_my_background(query: str) -> str:
    """Search the candidate's resume/background for relevant information based on the query."""
    vs = get_vectorstore()
    if vs is None:
        return "No resume vectorstore found. Please ingest a resume first."

    retriever = vs.as_retriever(search_kwargs={"k": 5})
    results = retriever.invoke(query)

    if not results:
        return "No relevant information found in the resume."

    return "\n\n".join(doc.page_content for doc in results)


@tool
def analyze_resume_ats(role_target: str = "General Software / AI Engineer") -> str:
    """
    Analyze the resume for ATS (Applicant Tracking System) compatibility, calculate an estimated ATS score (0-100),
    highlight formatting strengths, missing keywords, and suggest high-impact bullet improvements.
    """
    vs = get_vectorstore()
    if vs is None:
        return "No resume found to analyze."

    # Retrieve broad context
    retriever = vs.as_retriever(search_kwargs={"k": 8})
    docs = retriever.invoke("skills, projects, experience, education, metrics, certifications")
    resume_context = "\n\n".join(doc.page_content for doc in docs)

    return f"""Target Role for ATS Analysis: {role_target}
Candidate Resume Content for Analysis:
{resume_context}

Perform an exhaustive ATS audit with:
1. Estimated ATS Score (out of 100) with grade (e.g. 88/100 - Strong).
2. Key Strengths (quantified impact, tech stack alignment).
3. Missing or Recommended Keywords for {role_target}.
4. Action Verb & Impact Metric Enhancements (before & after examples).
5. Formatting & Readability Check for automated ATS parsers."""


@tool
def match_job_description(job_description: str) -> str:
    """
    Compare the candidate's resume against a given Job Description (JD).
    Calculates a Match Percentage, highlights matching skills, identifies missing requirements,
    and provides tailored talking points for the interview.
    """
    vs = get_vectorstore()
    if vs is None:
        return "No resume found to compare."

    # Retrieve relevant resume parts matching the JD
    retriever = vs.as_retriever(search_kwargs={"k": 6})
    matched_docs = retriever.invoke(job_description[:500])
    resume_summary = "\n\n".join(doc.page_content for doc in matched_docs)

    return f"""Job Description to Match:
{job_description}

Candidate Profile Context:
{resume_summary}

Analyze the alignment and provide:
1. Match Percentage (%) with breakdown (Skills, Experience, Education).
2. Exact Matching Qualifications found in resume.
3. Critical Missing Skills / Gaps to address.
4. Top 3 Positioning Strategies to highlight for this specific job application."""


@tool
def generate_mock_interview(role_or_focus: str = "AI / ML Engineer") -> str:
    """
    Generate tailored technical, architectural, and behavioral interview questions based on the candidate's actual projects and experience,
    accompanied by ideal STAR-method sample answer blueprints.
    """
    vs = get_vectorstore()
    if vs is None:
        return "No resume found to base interview on."

    retriever = vs.as_retriever(search_kwargs={"k": 6})
    docs = retriever.invoke("projects built, machine learning models, programming languages, algorithms")
    resume_context = "\n\n".join(doc.page_content for doc in docs)

    return f"""Role Focus: {role_or_focus}
Resume Details:
{resume_context}

Generate a comprehensive Mock Interview simulation:
1. 2 In-depth Technical Questions specifically probing candidate's projects (e.g. fraud detection, RAG, voice assistant).
2. 2 System Design / Architecture Questions relevant to their skill set.
3. 2 Behavioral (STAR Method) Questions.
4. Ideal Answer Frameworks with key talking points candidate should mention."""


@tool
def create_cold_email_cover_letter(target_company_or_role: str) -> str:
    """
    Generate a high-converting recruiter cold outreach email and a customized Cover Letter
    tailored specifically with projects and achievements from the candidate's resume.
    """
    vs = get_vectorstore()
    if vs is None:
        return "No resume found to craft outreach."

    retriever = vs.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke("achievements, projects, skills, education")
    resume_context = "\n\n".join(doc.page_content for doc in docs)

    return f"""Target Company / Role: {target_company_or_role}
Candidate Resume Context:
{resume_context}

Generate:
1. Subject line & concise, high-converting Cold Email to Hiring Manager (under 150 words).
2. Professional, compelling Cover Letter highlighting 2 flagship projects and quantified achievements."""