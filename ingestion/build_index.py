import os
import glob
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(_BASE_DIR, "data")
FAISS_DIR = os.path.join(_BASE_DIR, "faiss_index")

def load_all_documents(data_dir=DATA_DIR):
    """Load all markdown, text, and PDF documents from the specified directory."""
    documents = []

    for filepath in glob.glob(os.path.join(data_dir, "*.md")) + glob.glob(os.path.join(data_dir, "*.txt")):
        try:
            loader = TextLoader(filepath, encoding="utf-8")
            documents.extend(loader.load())
        except Exception as e:
            print(f"Error loading {filepath}: {e}")

    for filepath in glob.glob(os.path.join(data_dir, "*.pdf")):
        try:
            loader = PyPDFLoader(filepath)
            documents.extend(loader.load())
        except Exception as e:
            print(f"Error loading {filepath}: {e}")

    return documents


def build_vector_index(data_dir=DATA_DIR, output_dir=FAISS_DIR):
    """
    Load documents from data_dir, chunk them, create embeddings,
    save to output_dir, and return (chunk_count, doc_count).
    """
    print(f"Loading documents from {data_dir}...")
    documents = load_all_documents(data_dir)
    if not documents:
        raise ValueError(f"No valid documents (.pdf, .md, .txt) found in {data_dir}")

    print(f"Loaded {len(documents)} document(s). Splitting...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    print("Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)
    print(f"Saving FAISS index to {output_dir}...")
    os.makedirs(output_dir, exist_ok=True)
    vectorstore.save_local(output_dir)
    print("Done! FAISS index created successfully.")

    return len(chunks), len(documents)


if __name__ == "__main__":
    chunks_len, docs_len = build_vector_index()
    print(f"Successfully indexed {docs_len} document(s) into {chunks_len} chunks.")
