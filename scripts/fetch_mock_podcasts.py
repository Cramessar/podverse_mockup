import requests
import json
import os

MOCK_API_URL = "https://listen-api-test.listennotes.com/api/v2/search?q=star+wars"

def search_podcasts(query):
    response = requests.get(f"{MOCK_API_URL}")
    data = response.json()
    podcasts = data.get("results", [])

    formatted = []
    for podcast in podcasts:
        formatted.append({
            "title": podcast.get("title_original", podcast.get("title", "Untitled")),
            "publisher": podcast.get("publisher_original", podcast.get("publisher", "Unknown Publisher")),
            "image": podcast.get("image", ""),
            "description": podcast.get("description_original", ""),
        })

    # Save to public/data/podcasts.json
    output_dir = os.path.join(os.path.dirname(__file__), "..", "public", "data")
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "podcasts.json"), "w", encoding="utf-8") as f:
        json.dump(formatted, f, indent=2)

    print(f"✅ Saved {len(formatted)} podcasts to public/data/podcasts.json")

search_podcasts("star wars")
