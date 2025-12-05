import os
from dotenv import load_dotenv

# Load env vars from .env (or set to defaults)
load_dotenv()

def get_api_key() -> str:
    return os.getenv("OPENAI_API_KEY", "cse476")
def get_api_base() -> str:
    return os.getenv("API_BASE", "http://10.4.58.53:41701/v1")
def get_model_name() -> str:
    return os.getenv("MODEL_NAME", "bens_model")
