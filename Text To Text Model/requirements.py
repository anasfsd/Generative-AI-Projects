# Set Groq API Key
os.environ["GROQ_API_KEY"] = ""
import os
from groq import Groq
import streamlit as st

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Function to generate response using Groq
def chat_with_llm(user_message, model="llama3-8b-8192"):
    try:
        # Send message to Groq LLM
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": user_message},
            ],
            model=model,
        )
        # Return the LLM's response
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Streamlit App
def main():
    st.title("Real-Time Text-to-Text Chatbot")
    st.write("Powered by Groq and deployed on Streamlit.")

    # Input text from the user
    user_input = st.text_input("You:", "")

    # Display bot's response
    if st.button("Send"):
        if user_input.strip():
            with st.spinner("Thinking..."):
                bot_response = chat_with_llm(user_input)
            st.text_area("Bot:", bot_response, height=150)

if __name__ == "__main__":
    main()
