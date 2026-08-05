import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader


#load
loader = TextLoader("data/fenil_resume (1).md", encoding="utf-8")
print("loading PDF.....")
documents = loader.load()
print(f"Loaded {len(documents)} pages.")

#split documents into chunks 


text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
print("Splitting documents...") 
chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks.")


print("Creating embeddings...")
#create embeddings

embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#store in FAISS


vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)
print("Saving FAISS index...")
#save index
vectorstore.save_local("faiss_index")
print("Done! FAISS index created successfully.")

vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
results = vectorstore.similarity_search("credit card fraud detection ", k=5)
for r in results:
    print(r.page_content)
    print("---")