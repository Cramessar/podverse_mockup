#app/services/feed_parser.py

import feedparser
from typing import List, Dict, Any
from uuid import uuid4

def parse_feed(feed_url: str) -> dict[str, Any]:
    """
    Parse a feed URL and return a dictionary of metadata.
    
    """
    parsed = feedparser.parse(feed_url)
    
    feed_data = {
        "bozo": parsed.bozo, # boolean result based on if feed had parsing problems
        "bozo_exception":str(parsed.bozo_exception) if parsed.bozo else None, # if bozo is true then stores the error as string
        "url": feed_url,
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
