import os
from dotenv import load_dotenv

load_dotenv()

MODEL = "GPT"

# LLM_CONFIG = {
#     "model": "gpt-4",
#     "temperature": 0.3,
#     "max_tokens": 500,
#     "api_key": os.getenv("OPENAI_API_KEY"),
# }

LLM_CONFIG = {
    "model": "gemma2:2b",
    "temperature": 0.3,
    "max_tokens": 500,
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",  # required, but unused
}
