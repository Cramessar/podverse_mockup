# ai/backend/utils/ollama_model_selector.py

import os
import requests

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_OLLAMA_MODEL", "gemma:latest")

def list_models():
    try:
        res = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        res.raise_for_status()
        data = res.json()
        models = [m["name"] for m in data.get("models", [])]
        print(f"[🧠] Available models: {models}")
        return models
    except Exception as e:
        print(f"[❌] Failed to list models from Ollama: {e}")
        return []

def get_default_model():
    models = list_models()
    return models[0] if models else DEFAULT_MODEL
