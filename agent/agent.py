import sys
import io
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent  # noqa: deprecated – langgraph.prebuilt is still the correct import
from agent.tools import search_my_background

# Fix Windows console encoding so special characters print correctly
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")  # type: ignore[attr-defined]

# ── LLM ────────────────────────────────────────────────────────────────────
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
    num_predict=512,
)

# ── Tools ──────────────────────────────────────────────────────────────────
tools = [search_my_background]

# ── System prompt ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are a helpful career assistant. "
    "You have access to a tool called `search_my_background` that searches the user's resume. "
    "Always use this tool to answer questions about projects, skills, education, or experience. "
    "Never return an empty response — always provide a complete, clear answer."
)

# ── Agent ──────────────────────────────────────────────────────────────────
# create_react_agent from langgraph.prebuilt — prompt kwarg accepted since langgraph ≥0.2
agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)


# ── Main ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    query = "give me best ai projects from my resume."
    print(f"Querying agent: '{query}'\n")

    try:
        response = agent.invoke({"messages": [HumanMessage(content=query)]})
        print("\n--- Agent Response ---")
        final_msg = response["messages"][-1]
        safe = final_msg.content.encode("utf-8", errors="replace").decode("utf-8")
        print(safe)
    except Exception as e:
        print(f"\n[ERROR] Agent failed: {e}")
        print("Tip: Make sure Ollama is running (`ollama serve`) and the model is pulled (`ollama pull llama3.1:8b`)")
