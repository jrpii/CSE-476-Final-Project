### System prompts for the agent (and helpers to get them).

# Dictionary of system prompts per domain, will expand upon later.
SYSTEM_PROMPTS = {
    "default": "You are a helpful assistant. Reply with only the final answer, no explanation.",
    "math": "You are a math problem solver. Provide only the final numeric answer.",
    "coding": "You are a coding assistant. Provide clear, concise code solutions.",
    "future_prediction": "You are a prediction assistant. Provide accurate predictions based on available information.",
    "planning": "You are a planning assistant. Provide clear, actionable plans.",
    "common_sense": "You are a common sense reasoning assistant. Provide logical answers based on common knowledge.",
    "general": "You are a helpful assistant that provides accurate answers."
}

def get_system_prompt(domain: str = None) -> str:
    if domain and domain in SYSTEM_PROMPTS:
        return SYSTEM_PROMPTS[domain]
    return SYSTEM_PROMPTS["default"]
