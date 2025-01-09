import os
from dotenv import load_dotenv

load_dotenv()

LLM_CONFIG = {
    "model": "gpt-4",
    "temperature": 0.3,
    "max_tokens": 500,
    "api_key": os.getenv("OPENAI_API_KEY"),
}