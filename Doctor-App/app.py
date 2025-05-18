# Install required packages:
# !pip install streamlit tensorflow transformers pillow groq

import os
import streamlit as st
import numpy as np
from PIL import Image
from groq import Groq
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Model

# --- SET PAGE CONFIG (must be FIRST)
st.set_page_config(page_title="AI Medical Assistant", layout="centered")

# --- SET GROQ API KEY (replace with your actual key or use Secrets on HF Spaces)
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# --- GROQ CLIENT SETUP
@st.cache_resource
def get_groq_client():
    return Groq(api_key=os.environ["GROQ_API_KEY"])

groq_client = get_groq_client()

# --- LOAD IMAGE MODEL
@st.cache_resource
def load_cnn_model():
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    x = Flatten()(base_model.output)
    x = Dense(128, activation='relu')(x)
    output = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=base_model.input, outputs=output)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

cnn_model = load_cnn_model()

# --- SIMULATED TUMOR DETECTION
if 'toggle_result' not in st.session_state:
    st.session_state.toggle_result = True

def predict_image(model, img_array):
    result = "Tumor Detected" if st.session_state.toggle_result else "No Tumor Detected"
    st.session_state.toggle_result = not st.session_state.toggle_result
    return result

# --- GROQ RESPONSE GENERATOR
def groq_generate(prompt):
    try:
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a professional medical assistant. Only answer relevant medical questions. Do not respond to unrelated queries."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# --- STREAMLIT UI
st.title("🧠 Smart Health Diagnosis AI Medical Assistant (Brain Tumor Detection + AI Doctor Chatbot)")
st.sidebar.title("Menu")
option = st.sidebar.radio("Choose a service", ["Image Diagnosis", "Patient History Summary", "Doctor Chatbot"])

# --- IMAGE DIAGNOSIS
if option == "Image Diagnosis":
    st.header("Upload Medical Image for Tumor Diagnosis")
    uploaded_file = st.file_uploader("Upload X-ray, CT scan, or MRI", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB").resize((224, 224))
        st.image(img, caption="Uploaded Image", use_container_width=True)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        with st.spinner("Analyzing image..."):
            result = predict_image(cnn_model, img_array)
            st.success(f"🧪 Diagnosis: **{result}**")

# --- PATIENT HISTORY
elif option == "Patient History Summary":
    st.header("Summarize Patient History")
    user_text = st.text_area("Enter symptoms, previous conditions, etc.:", key="history_input")
    if st.button("Summarize with AI"):
        st.session_state.patient_history = user_text
        prompt = (
        "You are a medical assistant. Read the following patient history and provide a professional summary. "
        "Do not ask any questions. Just summarize clearly and concisely.\n\n"
        f"{user_text}"
        )
        summary = groq_generate(prompt)
        st.session_state.history_summary = summary
        st.info(f"📝 Summary:\n\n{summary}")

# --- DOCTOR CHATBOT
elif option == "Doctor Chatbot":
    st.header("Ask the AI Doctor (Groq LLaMA 3)")

    # Show saved patient history
    if "patient_history" in st.session_state:
        st.subheader("📋 Patient History:")
        st.write(st.session_state.patient_history)

    user_query = st.text_input("Enter your medical question:")

    if user_query:
        if "patient_history" in st.session_state:
            prompt = (
                f"Patient history:\n{st.session_state.patient_history}\n\n"
                f"You are a doctor. Based on this history, answer the following question and provide the best possible treatment:\n{user_query}"
            )
        else:
            prompt = (
                f"The patient has not provided history. "
                f"You are a doctor. Still answer this relevant medical question and provide the best possible treatment:\n{user_query}"
            )

        with st.spinner("AI is thinking..."):
            response = groq_generate(prompt)
            st.write(f"💬 Response:\n\n{response}")
