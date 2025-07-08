# ai/backend/utils/report_generator.py
import os
import requests
from sqlalchemy.orm import Session
from ai.backend.models import AIChannelProfile
from ai.backend.db import SessionLocal
import json
from datetime import datetime

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")


def fetch_profile_by_id(channel_id: int) -> dict:
    """Fetch channel profile from DB and make it JSON-serializable."""
    session: Session = SessionLocal()
    try:
        profile = session.query(AIChannelProfile).filter_by(id=channel_id).first()
        if not profile:
            raise ValueError(f"No profile found for channel_id {channel_id}")

        data = {}
        for key, value in profile.__dict__.items():
            if key.startswith("_"):
                continue
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            else:
                data[key] = value

        return data
    finally:
        session.close()

def build_chunks(profile: dict, max_chunk_size=2000):
    """Breaks down a large prompt into manageable character chunks."""
    intro = (
        "You are an expert systems analyst.\n\n"
        "Given the following podcast profile in JSON format, write a markdown-formatted report.\n\n"
        "Include these sections:\n"
        "1. Health Check\n"
        "2. Missing Data\n"
        "3. Optimization Suggestions\n"
        "Respond only in markdown format.\n"
    )
    
    profile_json = json.dumps(profile, indent=2)
    combined = f"{intro}\n\nPodcast Profile:\n{profile_json}"

    sentences = combined.split(". ")
    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) < max_chunk_size:
            current += sentence + ". "
        else:
            chunks.append(current.strip())
            current = sentence + ". "

    if current:
        chunks.append(current.strip())

    return chunks


def generate_report(channel_id: int, model: str = "mistral") -> str:
    profile_data = fetch_profile_by_id(channel_id)
    chunks = build_chunks(profile_data)

    responses = []
    for i, chunk in enumerate(chunks):
        try:
            res = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={"model": model, "prompt": chunk, "stream": False},
                timeout=30,
            )
            res.raise_for_status()
            data = res.json()
            responses.append(f"\n\n## Chunk {i+1}\n" + data.get("response", "[❌] No response"))
        except Exception as e:
            responses.append(f"\n\n## Chunk {i+1} failed\n[❌] {str(e)}")

    return "\n".join(responses)
