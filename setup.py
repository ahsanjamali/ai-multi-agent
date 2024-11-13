import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Verify API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("API key loaded successfully")
else:
    raise ValueError("API key not found. Please check your .env file")

# Make the API key available to OpenAI
os.environ["OPENAI_API_KEY"] = api_key