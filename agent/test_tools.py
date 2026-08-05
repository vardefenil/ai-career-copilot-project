from agent.tools import vectorstore

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

docs = retriever.invoke("List all the projects in my resume.")

print(f"Retrieved {len(docs)} documents\n")

for i, doc in enumerate(docs, 1):
    print(f"===== Document {i} =====")
    print(doc.page_content)
    print("-" * 60)
    