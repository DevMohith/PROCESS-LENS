import os, requests

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
APP_URL   = os.getenv("APP_URL", "http://localhost:8000")
APP_TITLE = os.getenv("APP_TITLE", "ProcessLens")
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")

def chat_complete(messages, model: str = None) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")   
    if not api_key:
        raise RuntimeError("Missing OPENROUTER_API_KEY")

    use_model = model or DEFAULT_MODEL
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": APP_URL,
        "X-Title": APP_TITLE,
    }
    payload = {"model": use_model, "messages": messages, "temperature": 0.2}
    resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
    if resp.status_code != 200:
        try: detail = resp.json()
        except: detail = resp.text
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {detail}")
    return resp.json()["choices"][0]["message"]["content"]
