# scripts/fetch_genres.py
import os
import requests
import json
from dotenv import load_dotenv

# Load env vars from .env.local
load_dotenv(dotenv_path=".env.local")

API_KEY = os.getenv("LISTENNOTES_API_KEY")

if not API_KEY:
    raise Exception("API key not found in environment")

headers = {
    "X-ListenAPI-Key": API_KEY
}

params = {
    "top_level_only": 1
}

url = "https://listen-api.listennotes.com/api/v2/genres"
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    genres = response.json()["genres"]
    with open("public/data/genres.json", "w", encoding="utf-8") as f:
        json.dump(genres, f, indent=2)
    print("✅ Genres saved to public/data/genres.json")
else:
    print(f"❌ Error {response.status_code}: {response.text}")
