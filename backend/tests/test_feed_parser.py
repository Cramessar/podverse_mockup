import pytest
from app.services.feed_parser import parse_rss_feed


def test_parse_rss_feed():
    test_url = "http://feeds.bbci.co.uk/news/rss.xml"

    # Call the parse_rss_feed function
    feed_info, items = parse_rss_feed(test_url)

    assert isinstance(feed_info, dict), "Feed info should be a dictionary"
    assert 'title' in feed_info, "Feed info should contain a title"
    assert isinstance(items, list), "Items should be a list"
    assert len(items) > 0, "Items list should not be empty"
    assert 'title' in items[0], "Each item should contain a title"
