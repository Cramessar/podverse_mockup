#app/services/feed_parser.py

import feedparser
import requests
from typing import List, Dict, Any
from uuid import uuid4
from urllib.parse import urlparse, urlunparse
from flask import current_app
import time

def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    normalized_path = parsed.path.replace('//', '/')
    return urlunparse(parsed._replace(path=normalized_path))

def parse_feed(feed_url: str) -> dict[str, Any]:
    """
    Parse a feed URL and return a dictionary of metadata.
    Normalizes the URL, attempts to fetch and parse the feed with timeout/retry,
    and logs key diagnostic data for error handling.
    """
    normalized_url = normalize_url(feed_url)
    
    # Get config values with defaults
    timeout = current_app.config.get('FEED_REQUEST_TIMEOUT', 10)
    retries = current_app.config.get('FEED_REQUEST_RETRIES', 2)
    
    parsed = None
    last_error = None
    
    # Retry logic with timeout
    for attempt in range(retries + 1):
        try:
            # Use requests with timeout, then pass content to feedparser
            response = requests.get(normalized_url, timeout=timeout, headers={
                'User-Agent': 'Podverse RSS Parser 1.0'
            })
            response.raise_for_status()
            
            # Parse the content with feedparser
            parsed = feedparser.parse(response.content)
            break  # Success, exit retry loop
            
        except requests.exceptions.RequestException as e:
            last_error = e
            if attempt < retries:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                time.sleep(wait_time)
                continue
            else:
                # Final attempt failed, fallback to feedparser's built-in fetch
                parsed = feedparser.parse(normalized_url)
    
    feed_data = {
        "bozo": parsed.bozo, # boolean result based on if feed had parsing problems
        "bozo_exception":str(parsed.bozo_exception) if parsed.bozo else None, # if bozo is true then stores the error as string
        "url": feed_url,
        "http_status": getattr(parsed, "status", None),
        "content_type": parsed.headers.get("content-type") if hasattr(parsed, "headers") else None
    }
    
    channel_data = {
        "title": parsed.feed.get("title")
    }
    
    items_data: List[Dict[str, Any]] = []
    for entry in parsed.entries: # each entry is a obj represents one item. parsed.entries is a list of these objects
        item = {
            "guid": entry.get("id") or entry.get("guid") or str(uuid4()), # maps to item.guid
            "title": entry.get("title"),
            "pub_date": entry.get("published"),
            "guid_enclosure_url": None
        }
        
        # If the entry has media attachments then extract the url of the first enclosure and map to guid_enclosure_url
        if "enclosures" in entry and entry.enclosures:
            item["guid_enclosure_url"] = entry.enclosures[0].get("href")
            
        items_data.append(item)
        
    return {
        "feed": feed_data,
        "channel": channel_data,
        "items": items_data
    }
