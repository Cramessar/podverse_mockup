# scripts/fetch_podcasts.py
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("LISTENNOTES_API_KEY")

if not api_key:
    raise ValueError("Missing LISTENNOTES_API_KEY in environment variables.")

url = "https://listen-api.listennotes.com/api/v2/search"

headers = {
    "X-ListenAPI-Key": api_key
}

params = {
    "q": "star wars",
    "type": "podcast",
    "language": "English",
    "len_min": 10,
    "len_max": 60
}

response = requests.get(url, headers=headers, params=params)
print(json.dumps(response.json(), indent=2))
