### Strait from notebook to test connection via CLI. (With exception of lines 9-13 where we import env vars from config.py)

# %% Minimal setup
# If needed (uncomment in a notebook):
# !pip install requests python-dotenv

import os, json, textwrap, re, time
import requests
from config import get_api_key, get_api_base, get_model_name

API_KEY = get_api_key()
API_BASE = get_api_base()
MODEL = get_model_name()

def call_model_chat_completions(prompt: str,
                                system: str = "You are a helpful assistant. Reply with only the final answer—no explanation.",
                                model: str = MODEL,
                                temperature: float = 0.0,
                                timeout: int = 60) -> dict:
    """
    Calls an OpenAI-style /v1/chat/completions endpoint and returns:
    { 'ok': bool, 'text': str or None, 'raw': dict or None, 'status': int, 'error': str or None, 'headers': dict }
    """
    url = f"{API_BASE}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type":  "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": 128,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
        status = resp.status_code
        hdrs   = dict(resp.headers)
        if status == 200:
            data = resp.json()
            text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {"ok": True, "text": text, "raw": data, "status": status, "error": None, "headers": hdrs}
        else:
            # try best-effort to surface error text
            err_text = None
            try:
                err_text = resp.json()
            except Exception:
                err_text = resp.text
            return {"ok": False, "text": None, "raw": None, "status": status, "error": str(err_text), "headers": hdrs}
    except requests.RequestException as e:
        return {"ok": False, "text": None, "raw": None, "status": -1, "error": str(e), "headers": {}}

# %% Direct call example
demo_prompt = "What is 17 + 28? Answer with just the number."
result = call_model_chat_completions(demo_prompt)
print("OK:", result["ok"], "HTTP:", result["status"])
print("MODEL SAYS:", (result["text"] or "").strip())

# Optional: Inspect rate-limit headers if your provider exposes them
for k in ["x-ratelimit-remaining-requests", "x-ratelimit-limit-requests", "x-request-id"]:
    if k in result["headers"]:
        print(f"{k}: {result['headers'][k]}")
