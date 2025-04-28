import streamlit as st
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import pipeline
import os

  # Use chroma_db locally, /app/chroma_db on Render
db_path = "/app/chroma_db" if os.getenv("RENDER") else "chroma_db"
if not os.path.exists(db_path):
    from scripts.build_vector_db import build_db
    build_db()

st.title("AI-Powered Code Explainer")
code_input = st.text_area("Enter your code snippet here:")
if st.button("Explain"):
    embeddings = HuggingFaceEmbeddings(model_name="distilgpt2")
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    query = f"Explain this Python code: {code_input}"
    docs = db.similarity_search(query, k=2)
    st.write("Retrieved documents:")
    for i, doc in enumerate(docs):
        st.write(f"Document {i}: {doc.page_content}")
    llm = HuggingFacePipeline.from_model_id(
          model_id="facebook/opt-125m",
          task="text-generation",
          device=-1,
          pipeline_kwargs={"max_new_tokens": 150, "truncation": True}
    )
    prompt = PromptTemplate(
          input_variables=["context", "question"],
          template="Context: {context}\n\nExplain this Python code in simple terms: {question}\n\nAnswer: "
  )
    context = "\n".join([doc.page_content for doc in docs])
    response = llm.invoke(prompt.format(context=context, question=query))
    st.write("Explanation:")
    st.write(response)