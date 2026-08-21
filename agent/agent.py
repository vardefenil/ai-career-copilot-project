"""
AI Career Copilot — Agent
Powered by Google Gemini 3.6 Flash via langchain-google-genai and LangGraph.
Equipped with 5 tools for resume Q&A, ATS scoring, Job Matching, Mock Interviews, and Outreach.
"""

import sys
import io
import os
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from agent.tools import (
    search_my_background,
    analyze_resume_ats,
    match_job_description,
    generate_mock_interview,
    create_cold_email_cover_letter,
)

# Fix Windows console encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")  # type: ignore[attr-defined]

# ── Gemini LLM ─────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not GEMINI_API_KEY:
    raise EnvironmentError(
        "Missing GEMINI_API_KEY in your .env file.\n"
        "Add: GEMINI_API_KEY=your_key_here"
    )

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
    max_output_tokens=2048,
)

# ── Tools ──────────────────────────────────────────────────────────────────
tools = [
    search_my_background,
    analyze_resume_ats,
    match_job_description,
    generate_mock_interview,
    create_cold_email_cover_letter,
]

# ── System prompt ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are the AI Career Copilot — an expert AI Career Coach, Technical Recruiter, and Career Advisor for Fenil Varde.
You have access to a suite of specialized career tools:
1. `search_my_background`: Search specific details from the resume (projects, skills, education, experience, achievements).
2. `analyze_resume_ats`: Perform an in-depth ATS (Applicant Tracking System) scan with scores (0-100), missing keywords, and improvements.
3. `match_job_description`: Compare resume against a Job Description to calculate match %, skill gaps, and custom talking points.
4. `generate_mock_interview`: Create custom technical, architectural, and behavioral interview questions tailored to the resume projects.
5. `create_cold_email_cover_letter`: Craft high-converting cold emails and tailored cover letters for hiring managers.

Guidelines:
- When asked general questions about skills/projects/background, use `search_my_background`.
- When asked for ATS scoring/review, invoke `analyze_resume_ats`.
- When given a Job Description or asked if qualified for a role, invoke `match_job_description`.
- When asked for interview preparation or mock questions, invoke `generate_mock_interview`.
- When asked for outreach, email, or cover letter, invoke `create_cold_email_cover_letter`.
- Format responses beautifully with markdown headers, bold highlights, clean bullet points, and actionable advice.
- Always provide insightful, encouraging, and highly professional career coaching."""

# ── Agent ──────────────────────────────────────────────────────────────────
agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)


# ── Main ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    query = "Analyze my resume for ATS readiness and calculate my score for an AI Engineer role."
    print(f"Querying agent: '{query}'\n")

    try:
        response = agent.invoke({"messages": [HumanMessage(content=query)]})
        print("\n--- Agent Response ---")
        final_msg = response["messages"][-1]
        content = final_msg.content
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    parts.append(item["text"])
                elif isinstance(item, str):
                    parts.append(item)
            content = "\n".join(parts)
        print(content)
    except Exception as e:
        print(f"\n[ERROR] Agent failed: {e}")
        print("Tip: Make sure GEMINI_API_KEY is set in your .env file.")
