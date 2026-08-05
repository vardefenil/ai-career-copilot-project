import io
import os
import sys
import warnings

# Suppress langchain-community deprecation — no standalone langchain-faiss package exists yet
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.tools import tool

# Fix Windows console encoding so special characters don't crash prints
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

print("1. Imports completed")

# Build absolute path to faiss_index regardless of working directory
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_FAISS_PATH = os.path.join(_BASE_DIR, "faiss_index")

# Load the index once, at module level (not inside the function)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("2. Embeddings loaded")
vectorstore = FAISS.load_local(_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
print("3. FAISS loaded")


@tool
def search_my_background(query: str) -> str:
    """Search the user's resume/background for relevant information based on the query."""
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )

    results = retriever.invoke(query)

    if not results:
        return "No relevant information found."

    return "\n\n".join(doc.page_content for doc in results)


if __name__ == "__main__":
    print("Testing retriever...")

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke("List all the projects in my resume.")

    print(f"Retrieved {len(docs)} documents")

    for i, doc in enumerate(docs, 1):
        print(f"\n===== Document {i} =====")
        # encode to utf-8, replace any unmappable chars
        safe_content = doc.page_content.encode("utf-8", errors="replace").decode("utf-8")
        print(safe_content)

    print("\n__name__ =", __name__)
    print("Running file:", __file__)
    print("Current working directory:", os.getcwd())