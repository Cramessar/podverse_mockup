#app/services/feed_parser.py

import feedparser
import requests
from typing import List, Dict, Any, Optional
from uuid import uuid4
from urllib.parse import urlparse, urlunparse
from flask import current_app
import time
from app.utils.error_exceptions import ParseError
from app.utils.logger import get_logger

logger = get_logger(__name__)

def normalize_url(url: str) -> str:
    """Normalize a URL by removing double slashes and standardizing format."""
    parsed = urlparse(url)
    normalized_path = parsed.path.replace('//', '/')
    return urlunparse(parsed._replace(path=normalized_path))

def parse_feed(feed_url: str) -> dict[str, Any]:
    """
    Parse a feed URL and return a dictionary of metadata.
    Handles various error cases and provides detailed error information.
    """
    normalized_url = normalize_url(feed_url)
    
    # Get config values with defaults
    timeout = current_app.config.get('FEED_REQUEST_TIMEOUT', 10)
    retries = current_app.config.get('FEED_REQUEST_RETRIES', 2)
    
    parsed: Optional[feedparser.FeedParserDict] = None
    last_error = None
    http_status = None
    content_type = None
    
    # Retry logic with timeout
    for attempt in range(retries + 1):
        try:
            # Use requests with timeout, then pass content to feedparser
            response = requests.get(normalized_url, timeout=timeout, headers={
                'User-Agent': 'Podverse RSS Parser 1.0'
            })
            http_status = response.status_code
            content_type = response.headers.get('content-type')
            
            response.raise_for_status()
            
            # Parse the content with feedparser
            parsed = feedparser.parse(response.content)
            
            # Check for basic feed validity
            if not hasattr(parsed, 'feed') or not parsed.feed:
                raise ParseError("Invalid feed format - no feed data found")
                
            if not hasattr(parsed, 'entries'):
                raise ParseError("Invalid feed format - no entries found")
                
            break  # Success, exit retry loop
            
        except requests.exceptions.RequestException as e:
            last_error = e
            logger.warning(f"Request failed for {normalized_url} (attempt {attempt + 1}/{retries + 1}): {str(e)}")
            
            if attempt < retries:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
                continue
            else:
                # Final attempt - try feedparser's built-in fetch
                try:
                    parsed = feedparser.parse(normalized_url)
                    if not hasattr(parsed, 'feed') or not parsed.feed:
                        raise ParseError("Invalid feed format - no feed data found")
                    if not hasattr(parsed, 'entries'):
                        raise ParseError("Invalid feed format - no entries found")
                    if parsed.bozo:
                        raise ParseError(f"Feed parsing error: {str(parsed.bozo_exception)}")
                except Exception as parser_error:
                    raise ParseError(f"Failed to fetch or parse feed: {str(last_error)}. Parser error: {str(parser_error)}")
    
    if not parsed:
        raise ParseError(f"Failed to parse feed after {retries + 1} attempts")
    
    feed_data = {
        "bozo": getattr(parsed, 'bozo', False),
        "bozo_exception": str(parsed.bozo_exception) if hasattr(parsed, 'bozo_exception') and parsed.bozo else None,
        "url": feed_url,
        "http_status": http_status or getattr(parsed, "status", None),
        "content_type": content_type or (parsed.headers.get("content-type") if hasattr(parsed, "headers") else None)
    }
    
    channel_data = {
        "title": getattr(parsed.feed, "title", "") or "",
        "description": getattr(parsed.feed, "description", "") or "",
        "link": getattr(parsed.feed, "link", "") or "",
        "language": getattr(parsed.feed, "language", "") or "",
        "copyright": getattr(parsed.feed, "copyright", "") or "",
        "last_build_date": getattr(parsed.feed, "updated", "") or ""
    }
    
    items_data: List[Dict[str, Any]] = []
    for entry in getattr(parsed, 'entries', []):
        item = {
            "guid": getattr(entry, "id", None) or getattr(entry, "guid", None) or str(uuid4()),
            "title": getattr(entry, "title", "") or "",
            "description": getattr(entry, "description", "") or "",
            "pub_date": getattr(entry, "published", "") or "",
            "link": getattr(entry, "link", "") or "",
            "author": getattr(entry, "author", "") or "",
            "guid_enclosure_url": None
        }
        
        if hasattr(entry, 'enclosures') and entry.enclosures:
            item["guid_enclosure_url"] = entry.enclosures[0].get("href")
            
        items_data.append(item)
    
    if not items_data:
        logger.warning(f"No items found in feed: {normalized_url}")
    
    return {
        "feed": feed_data,
        "channel": channel_data,
        "items": items_data
    }
