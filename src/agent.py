### Simple agent for making LLM API calls.
import requests
from scripts.config import get_api_key, get_api_base, get_model_name

API_KEY = get_api_key()
API_BASE = get_api_base()
MODEL = get_model_name()

# Simple agent call to LLM API.
def call_agent(system_prompt: str, user_message: str, max_tokens: int = 512, temperature: float = 0.0, timeout: int = 120) -> dict:
    # Build request URL and headers (like notebook).
    url = f"{API_BASE}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    # Try to make the request (again like the notebook).
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {"ok": True, "text": text.strip() if text else None, "error": None}
        else:
            # try best-effort to surface error text
            try:
                error_text = resp.json()
            except:
                error_text = resp.text
            return {"ok": False, "text": None, "error": str(error_text)}
    except requests.RequestException as e:
        return {"ok": False, "text": None, "error": str(e)}
