import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AIRVISUAL_API_KEY = os.getenv("AIRVISUAL_API_KEY")

# Other configuration settings
DEFAULT_MODEL = "llama3-70b-8192" 
