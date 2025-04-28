from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings 
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") 
db = Chroma(persist_directory="chroma_db", embedding_function=embeddings) 
query = "Explain this Python code: for i in range(5): print(i)" 
results = db.similarity_search_with_score(query, k=2) 
print("Retrieved documents:") 
for i, (doc, score) in enumerate(results): 
    print(f"[{i}]: {doc.page_content} (Score: {score})") 
