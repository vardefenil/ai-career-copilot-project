"""
AI Career Copilot — Agent
Now powered by Google Gemini (gemini-1.5-flash) via langchain-google-genai.
Falls back gracefully if API key is missing.
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
from agent.tools import search_my_background

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
    temperature=0,
    max_output_tokens=1024,
)

# ── Tools ──────────────────────────────────────────────────────────────────
tools = [search_my_background]

# ── System prompt ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are a helpful AI Career Copilot for Fenil Varde. "
    "You have access to a tool called `search_my_background` that searches Fenil's resume. "
    "Always use this tool to answer questions about projects, skills, education, experience, or achievements. "
    "Provide clear, well-formatted, complete answers. Use bullet points and bold text where helpful. "
    "Never return an empty response."
)

# ── Agent ──────────────────────────────────────────────────────────────────
agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)


# ── Main ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    query = "List all AI projects from my resume with tech stack details."
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
