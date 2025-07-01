# app/services/feed_parser.py

import feedparser
from typing import List, Dict, Any
from uuid import uuid4  # Missing import for uuid4

def parse_rss_feed(feed_url: str) -> dict[str, Any]:
    """
    Parse a feed URL and return a dictionary of metadata.
    """
    parsed = feedparser.parse(feed_url)

    feed_data = {
        "bozo": parsed.bozo,
        "bozo_exception": str(parsed.bozo_exception) if parsed.bozo else None,
        "url": feed_url,
    }

    channel_data = {
        "title": parsed.feed.get("title")
    }

    items_data: List[Dict[str, Any]] = []

    for entry in parsed.entries:
        item = {
            "guid": entry.get("id") or entry.get("guid") or str(uuid4()),
            "title": entry.get("title"),
            "pub_date": entry.get("published"),
            "guid_enclosure_url": None,
        }

        if "enclosures" in entry and entry.enclosures:
            item["guid_enclosure_url"] = entry.enclosures[0].get("href")

        items_data.append(item)

    return {
        "feed": feed_data,
        "channel": channel_data,
        "items": items_data,
    }
