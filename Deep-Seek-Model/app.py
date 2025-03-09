import streamlit as st
import subprocess
import time
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)
import httpx

# Function to check if Ollama is running
def is_ollama_running():
    try:
        subprocess.run(["ollama", "list"], check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to start Ollama server if not running
def start_ollama():
    if not is_ollama_running():
        st.warning("🛠️ Ollama is not running. Attempting to start it...")
        subprocess.Popen(["ollama", "serve"])
        time.sleep(5)  # Wait for Ollama to start
        if is_ollama_running():
            st.success("✅ Ollama started successfully!")
        else:
            st.error("❌ Failed to start Ollama. Please start it manually.")

# Check and start Ollama
start_ollama()

# Custom CSS for dark theme
st.markdown("""
<style>
    .main { background-color: #1a1a1a; color: #ffffff; }
    .sidebar .sidebar-content { background-color: #2d2d2d; }
    .stTextInput textarea { color: #ffffff !important; }
    .stSelectbox div[data-baseweb="select"] { color: white !important; background-color: #3d3d3d !important; }
    .stSelectbox svg { fill: white !important; }
    div[role="listbox"] div { background-color: #2d2d2d !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

st.title("🩺 DeepSeek Doctor")
st.caption("🚀 Your AI Medical Assistant")

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Configuration")
    selected_model = st.selectbox(
        "Choose Model",
        ["deepseek-r1:1.5b", "deepseek-r1:3b"],
        index=0
    )
    st.divider()
    st.markdown("### Model Capabilities")
    st.markdown("""
    - 🩺 Medical Diagnosis
    - 📊 Symptom Analysis
    - 💡 Health Advice
    """)
    st.divider()
    st.markdown("Built with [Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/)")

# Ensure the model is downloaded
st.info(f"🛠️ Checking if `{selected_model}` is available...")
subprocess.run(["ollama", "pull", selected_model], check=True)

# Initialize ChatOllama
try:
    llm_engine = ChatOllama(
        model=selected_model,
        base_url="http://localhost:11434",
        temperature=0.3
    )
except httpx.ConnectError:
    st.error("❌ Error connecting to Ollama. Please ensure the server is running.")

# System prompt configuration
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an experienced and compassionate doctor with expertise in diagnosing medical conditions "
    "and providing evidence-based advice. Always base your responses on medical best practices."
)

# Session state management
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Hi! I'm DeepSeek. How can I help you today?"}]

# Chat container
chat_container = st.container()
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Function to generate AI response
def generate_ai_response(prompt_chain):
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({})

# Function to build chat prompt
def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

# User input handling
user_query = st.chat_input("Type your medical question here...")
if user_query:
    st.session_state.message_log.append({"role": "user", "content": user_query})
    with st.spinner("🧠 Processing..."):
        prompt_chain = build_prompt_chain()
        try:
            ai_response = generate_ai_response(prompt_chain)
        except httpx.ConnectError:
            st.error("❌ Unable to connect to Ollama. Make sure it is running.")
            ai_response = "I'm currently unavailable. Please try again later."
    st.session_state.message_log.append({"role": "ai", "content": ai_response})
    st.rerun()
