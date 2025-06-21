import streamlit as st
from groq import Groq
from streamlit_ace import st_ace
from datetime import datetime
import time

# --- Constants ---
THEMES = ["monokai", "github", "twilight"]
LANGUAGES = ["python", "javascript", "java", "c", "cpp"]

# --- Groq Client Setup ---
client = Groq(api_key="")  # Replace with your actual key

# --- Page Config ---
st.set_page_config(
    page_title="🔍 CodeMedic AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Session State ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'processing' not in st.session_state:
    st.session_state.processing = False

# --- UI Components ---
def gradient_text(text):
    return f"""
    {text}
    """

# --- Sidebar ---
with st.sidebar:
    st.markdown(gradient_text("CodeMedic AI"), unsafe_allow_html=True)
    st.markdown("---")

    with st.expander("⚙️ Settings"):
        selected_theme = st.selectbox("Editor Theme", THEMES, index=0)
        selected_lang = st.selectbox("Code Language", LANGUAGES, index=0)
        model_temp = st.slider("🧠 AI Creativity", 0.0, 1.0, 0.7)

    st.markdown("---")
    st.button("🧹 Clear History", on_click=lambda: st.session_state.history.clear())
    st.markdown(f"Session Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", unsafe_allow_html=True)

# --- Main Title ---
st.markdown(gradient_text("Code Diagnostics Suite"), unsafe_allow_html=True)
st.markdown("AI-powered code analysis with deep error detection and fix generation", unsafe_allow_html=True)

# --- Code Editor ---
with st.container(border=True):
    code = st_ace(
        placeholder=f"Enter {selected_lang} code...",
        language=selected_lang,
        theme=selected_theme,
        height=400,
        key=f"ace_{selected_lang}",
        wrap=True
    )

# --- Analysis Controls ---
col1, col2 = st.columns([1, 3])
with col1:
    analyze_btn = st.button("🚀 Analyze Code", use_container_width=True)
with col2:
    if st.session_state.processing:
        st.warning("AI is analyzing code...")

# --- Analysis Logic ---
if analyze_btn and not st.session_state.processing:
    if not code.strip():
        st.error("⚠️ Please enter valid code")
    else:
        st.session_state.processing = True
        try:
            with st.spinner("🔍 Deep code analysis in progress..."):
                start_time = time.time()
                response = client.chat.completions.create(
                    messages=[{
                        "role": "system",
                        "content": (
                            "You are an expert static code analyzer. Your only job is to analyze code for:\n"
                            "1. Syntax validation\n2. Logical error detection\n"
                            "3. Security vulnerabilities\n4. Optimization suggestions\n\n"
                            "IMPORTANT:\n"
                            "- Only respond with code-related analysis.\n"
                            "- Do NOT respond to general questions.\n"
                            "- If the user input is not code or code-related, reply with:\n"
                            "  '⚠️ Please input code to analyze. I only respond to code-related requests.'"
                        )
                    }, {
                        "role": "user",
                        "content": code
                    }],
                    model="llama3-70b-8192",
                    temperature=model_temp
                )
                analysis = response.choices[0].message.content
                duration = time.time() - start_time

                st.session_state.history.append({
                    "timestamp": datetime.now().isoformat(),
                    "code": code,
                    "analysis": analysis,
                    "language": selected_lang,
                    "duration": f"{duration:.2f}s"
                })

            st.success("✅ Analysis Complete")
            st.markdown("### 📝 Analysis Report")
            st.markdown(analysis)

        except Exception as e:
            st.error(f"❌ Analysis Failed: {str(e)}")

        finally:
            st.session_state.processing = False

# --- History Section ---
if st.session_state.history:
    st.markdown("## 📜 Analysis History")
    for entry in reversed(st.session_state.history):
        with st.container(border=True):
            cols = st.columns([1, 3, 1])
            cols[0].markdown(f"**Language**: {entry['language']}")
            cols[1].markdown(f"**Time**: {entry['timestamp']}")
            cols[2].markdown(f"**Duration**: {entry['duration']}")

            st.markdown("**Code:**")
            st.code(entry['code'], language=entry['language'])

            st.markdown("**Analysis:**")
            st.markdown(entry['analysis'])

# --- Footer ---
st.markdown("---")
st.markdown("""

    
        Powered by Groq
        •
        Documentation
        •
        Feedback
    
    Made with ❤️ by AI Code Experts

""", unsafe_allow_html=True)
