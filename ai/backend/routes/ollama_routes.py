# ai/backend/routes/ollama_routes.py
from flask import Blueprint, jsonify, request
from ai.backend.utils.ollama_client import get_available_ollama_models

ollama_bp = Blueprint("ollama", __name__, url_prefix="/ollama")

@ollama_bp.route("/models", methods=["GET"])
def list_models():
    """
    Returns a list of available Ollama models.
    """
    models = get_available_ollama_models()
    return jsonify({"available_models": models}), 200

@ollama_bp.route("/status", methods=["GET"])
def ollama_status():
    """
    Health check route to verify Ollama container accessibility.
    """
    models = get_available_ollama_models()
    if models:
        return jsonify({"status": "online", "model_count": len(models)}), 200
    return jsonify({"status": "offline", "error": "No models detected"}), 503
