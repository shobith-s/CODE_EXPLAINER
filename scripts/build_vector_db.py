from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

def build_db():
    loader = TextLoader("data/python_docs.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(docs, embeddings, persist_directory="chroma_db")
    print(f"Documents in database: {len(docs)}")
    for i, doc in enumerate(docs):
        print(f"Document {i}: {doc.page_content[:100]}...")
    print("Vector database built successfully.")

if __name__ == "__main__":
      build_db()