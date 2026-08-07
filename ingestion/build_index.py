import os
import glob
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
#all documents can load
DATA_DIR = "data"

def load_all_documents(data_dir):
    documents = []

    for filepath in glob.glob(os.path.join(data_dir, "*.md")) + glob.glob(os.path.join(data_dir, "*.txt")):
        print(f"Loading: {filepath}")
        loader = TextLoader(filepath, encoding="utf-8")
        documents.extend(loader.load())

    for filepath in glob.glob(os.path.join(data_dir, "*.pdf")):
        print(f"Loading: {filepath}")
        loader = PyPDFLoader(filepath)
        documents.extend(loader.load())

    return documents

print("Loading all documents from data/ ...")
documents = load_all_documents(DATA_DIR)
print(f"Loaded {len(documents)} document(s) total.")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
print("Splitting documents...")
chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks.")

print("Creating embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)
print("Saving FAISS index...")
vectorstore.save_local("faiss_index")
print("Done! FAISS index created successfully.")
