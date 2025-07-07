import streamlit as st
from datetime import datetime
import pandas as pd
import os

# LangChain & PDF/CSV Loader Imports
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import LlamaCpp
from langchain.chains import RetrievalQA

# 🔒 Authentication Check
if not st.session_state.get("authenticated"):
    st.error("Please login first.")
    st.stop()

# 💠 Styling
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.ytimg.com/vi/Dcemvtppdfg/maxresdefault.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Ask the ISRO AI Agent")
query = st.text_input("Enter your question about ISRO:")

# 📄 Load documents safely
def load_data():
    documents = []

    if os.path.exists("data/ISRO.pdf") and os.path.getsize("data/ISRO.pdf") > 0:
        try:
            pdf_loader = PyPDFLoader("data/ISRO.pdf")
            documents.extend(pdf_loader.load_and_split())
        except Exception as e:
            st.warning(f"Error loading PDF: {e}")

    if os.path.exists("data/satellites.csv") and os.path.getsize("data/satellites.csv") > 0:
        try:
            csv_loader = CSVLoader(file_path="data/satellites.csv")
            documents.extend(csv_loader.load())
        except Exception as e:
            st.warning(f"Error loading CSV: {e}")

    if not documents:
        st.error("No valid documents found in /data. Please check your files.")
        st.stop()

    return documents

# 🧠 Create vector store
def create_vector_store(documents):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

# 🦙 LLM and QA chain setup
@st.cache_resource
def get_qa_chain():
    documents = load_data()
    vectorstore = create_vector_store(documents)
    retriever = vectorstore.as_retriever()

    llm = LlamaCpp(
        model_path="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        n_ctx=2048,
        temperature=0.5,
        max_tokens=512,
        verbose=True
    )

    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa

# 🧠 Run Query and Log
if query:
    qa_chain = get_qa_chain()
    with st.spinner("🔍 Thinking..."):
        result = qa_chain.run(query)

    st.success(result)

    # ✅ Log user query and response
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "email": st.session_state.get("user_email", "unknown"),
        "query": query,
        "response": result
    }

    os.makedirs("logs", exist_ok=True)
    log_path = "logs/user_logs.csv"

    if not os.path.exists(log_path):
        pd.DataFrame([log_entry]).to_csv(log_path, index=False)
    else:
        pd.DataFrame([log_entry]).to_csv(log_path, mode='a', header=False, index=False)

    
