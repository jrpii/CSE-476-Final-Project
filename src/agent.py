### Simple agent for making LLM API calls and related helpers.
import requests
from scripts.config import get_api_key, get_api_base, get_model_name

API_KEY = get_api_key()
API_BASE = get_api_base()
MODEL = get_model_name()

# Domain and difficulty labels.
DOMAINS = ["math", "coding", "future_prediction", "planning", "common_sense"]
COMPLEXITY_LEVELS = ["easy", "medium", "hard", "extremely hard"]

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

# Have model infere domain lavel from question.
def guess_domain(text: str) -> str:
    system_prompt = (
        "You are a classifier that assigns a single domain label to a question. "
        "Possible domain labels are: math, coding, future_prediction, planning, common_sense. "
        "Reply with exactly one of these labels and nothing else."
    )
    user_message = (
        "Question:\n"
        f"{text}\n\n"
        "Choose the single best domain label from: math, coding, future_prediction, "
        "planning, common_sense, general.\n"
        "Reply with exactly one domain label (for example: math)."
    )
    
    resp = call_agent(system_prompt=system_prompt, user_message=user_message, max_tokens=8)
    if not resp["ok"] or not resp.get("text"):
        return "general"

    label = resp["text"].strip().split()[0].lower()
    return label if label in DOMAINS else "general"

# Have model infere complexity level from question.
def guess_complexity(text: str) -> str:
    system_prompt = (
        "You are a difficulty classifier for questions. "
        "Choose exactly one label from: easy, medium, hard, extremely hard. "
        "Reply with only that label and nothing else."
    )
    user_message = (
        "Question:\n"
        f"{text}\n\n"
        "Classify the difficulty of this question as exactly one of: "
        "easy, medium, hard, extremely hard.\n"
        "Reply with just that single label."
    )

    resp = call_agent(system_prompt=system_prompt, user_message=user_message, max_tokens=8)
    if not resp["ok"] or not resp.get("text"):
        return "medium"

    label = resp["text"].strip().lower().split()[0]
    return label if label in COMPLEXITY_LEVELS else "medium"
