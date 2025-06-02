import streamlit as st
import time
import random
import os
from pymongo import MongoClient
from config import database_url
from app.llm.rag_system import load_data_embedding, pdfLoader, text_spliter



if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "file_text" not in st.session_state:
    st.session_state.file_text = ""

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

def extract_text_from_pdf(file):
    return "demo"

# --- Helper: Extract text from DOCX ---
def extract_text_from_docx(file):
    return "hello"


def save_uploaded_file_locally(uploaded_file, folder="uploads"):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path



def streamlit_chat_interface(user_info):
    # Initialize chat history
    st.sidebar.header("📎 Upload Document")
    uploaded_file = st.sidebar.file_uploader("Upload PDF or Word file", type=["pdf", "docx"])

    if uploaded_file:
        with st.spinner("🔄 Uploading and processing file..."):
            # Your file processing logic here
            file_path = save_uploaded_file_locally(uploaded_file)
        st.success(f"✅ Saved file to the directory {file_path}")
        file_type = uploaded_file.type

        if file_type == "application/pdf":
            text = pdfLoader(file_path)
        elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            text = extract_text_from_docx(uploaded_file)
        else:
            st.sidebar.error("Unsupported file type")
            text = ""
            
        with st.spinner("🔪 Splitting text..."):
            raw_text = text_spliter(text)    
        
        if raw_text:
            st.session_state.file_text = raw_text
            st.success("✅ File uploaded and processed!")
            
        with st.spinner("🧠 Creating embeddings and uploading to Pinecone..."):
            load_data_embedding(raw_text)
            st.success("✅ Embeddings created and uploaded to Pinecone!")
    # --- Display Preview ---
    if "file_text" in st.session_state:

        # --- Chat Interface ---
        st.subheader("💬 lets ask the bot now")
        user_input = st.chat_input("Ask something about the file...")

        if user_input:
            # 🔁 Simple mock response (replace with real LLM logic)
            response = f"I received your question: '{user_input}'.\n\nUnfortunately, I am just a demo bot right now 😅"

            # Append to chat history
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("bot", response))

        # --- Display Chat ---
        if "chat_history" in st.session_state:
            for role, msg in st.session_state.chat_history:
                with st.chat_message(role):
                    st.markdown(msg)
    else:
        st.info("⬅️ Upload a file to begin.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
