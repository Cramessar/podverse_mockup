## ai/backend/utils/ollama_client.py

import requests

OLLAMA_API_URL = "http://ollama:11434/api/tags"

def get_available_ollama_models():
    try:
        response = requests.get(OLLAMA_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        models = data.get("models", [])
        return [model["name"] for model in models]
    except requests.RequestException as e:
        print(f"[Ollama Error] Could not fetch models: {e}")
        return []
