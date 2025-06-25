import pytest
from app.models.feed import Feed
from app.models.channel import Channel

@pytest.fixture
def sample_feed(db):
    """Create a sample feed for testing."""
    channel = Channel(
        title="Test Channel",
        description="Test Description"
    )
    db.session.add(channel)
    
    feed = Feed(
        url="http://example.com/feed.xml",
        channel=channel
    )
    db.session.add(feed)
    db.session.commit()
    return feed

@pytest.fixture
def sample_feed_data():
    """Sample feed data for testing."""
    return {
        "url": "http://example.com/feed.xml",
        "title": "Test Feed",
        "description": "Test Feed Description"
    } 