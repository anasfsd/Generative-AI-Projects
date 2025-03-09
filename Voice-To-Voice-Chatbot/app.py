# Import libraries
import whisper
import os
from gtts import gTTS
import gradio as gr
from groq import Groq

# Load Whisper model for transcription
model = whisper.load_model("base")

# Set up Groq API client (ensure GROQ_API_KEY is set in your environment)
client = Groq(api_key=os.environ.get(" "))

# Function to get the LLM response from Groq
def get_llm_response(user_input):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="llama3-8b-8192",  # Replace with your desired model
    )
    return chat_completion.choices[0].message.content

# Function to convert text to speech using gTTS
def text_to_speech(text, output_audio="output_audio.mp3"):
    tts = gTTS(text)
    tts.save(output_audio)
    return output_audio

# Main chatbot function to handle audio input and output
def chatbot(audio):
    # Step 1: Transcribe the audio using Whisper
    result = model.transcribe(audio)
    user_text = result["text"]

    # Step 2: Get LLM response from Groq
    response_text = get_llm_response(user_text)

    # Step 3: Convert the response text to speech
    output_audio = text_to_speech(response_text)
    
    return response_text, output_audio

# Gradio interface for real-time interaction
iface = gr.Interface(
    fn=chatbot,
    inputs=gr.Audio(type="filepath"),  # Input from mic or file
    outputs=[gr.Textbox(), gr.Audio(type="filepath")],  # Output: response text and audio
    live=True
)

# Launch the Gradio app
iface.launch()
