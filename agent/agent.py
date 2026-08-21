"""
AI Career Copilot — Agent
Powered by Google Gemini 3.6 Flash via langchain-google-genai and LangGraph.
Equipped with 5 specialized tools and MemorySaver checkpointer for thread_id session memory.
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
from langgraph.checkpoint.memory import MemorySaver

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

# ── Checkpointer for multi-turn session threads ────────────────────────────
checkpointer = MemorySaver()

# ── System prompt ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are the AI Career Copilot — an expert AI Career Coach, Technical Recruiter, and Career Advisor for Fenil Varde.
You have access to a suite of specialized career tools:
1. `search_my_background`: Search specific details from the resume (projects, skills, education, experience, achievements).
2. `analyze_resume_ats`: Perform an in-depth ATS (Applicant Tracking System) scan with scores (0-100), missing keywords, and improvements. Output tables when comparing categories.
3. `match_job_description`: Compare resume against a Job Description to calculate match %, skill gaps, and custom talking points.
4. `generate_mock_interview`: Create custom technical, architectural, and behavioral interview questions tailored to the resume projects.
5. `create_cold_email_cover_letter`: Craft high-converting cold emails and tailored cover letters for hiring managers.

Guidelines:
- When asked general questions about skills/projects/background, use `search_my_background`.
- When asked for ATS scoring/review, invoke `analyze_resume_ats`.
- When given a Job Description or asked if qualified for a role, invoke `match_job_description`.
- When asked for interview preparation or mock questions, invoke `generate_mock_interview`.
- When asked for outreach, email, or cover letter, invoke `create_cold_email_cover_letter`.
- Maintain conversational context across questions within the same thread.
- Format responses beautifully with clean markdown tables, headers, bold text, and bullet points.
- Always provide insightful, encouraging, and highly professional career coaching."""

# ── Agent with Checkpointer ────────────────────────────────────────────────
agent = create_react_agent(
    llm,
    tools,
    prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)


# ── Helper invocation function ─────────────────────────────────────────────
def query_agent(query: str, thread_id: str = "default") -> str:
    """Invoke the agent with thread-specific session context."""
    config = {"configurable": {"thread_id": thread_id}}
    response = agent.invoke({"messages": [HumanMessage(content=query)]}, config=config)
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

    return str(content)


# ── Main test ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_thread = "test-session-1"
    q1 = "What are the main projects on my resume?"
    print(f"Query 1 ({test_thread}): {q1}\n")
    ans1 = query_agent(q1, thread_id=test_thread)
    print(ans1)

    q2 = "Which of those projects uses scikit-learn?"
    print(f"\nQuery 2 ({test_thread}): {q2}\n")
    ans2 = query_agent(q2, thread_id=test_thread)
    print(ans2)
