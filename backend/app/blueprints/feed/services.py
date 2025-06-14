from app.models.feed import Feed
from app.extensions import db
from typing import List, Optional

class FeedService:
    """Service layer for Feed operations - minimal factory pattern implementation"""

    @staticmethod
    def get_all_feeds() -> List[Feed]:
        return Feed.query.all()

    @staticmethod
    def get_feed_by_id(feed_id: int) -> Optional[Feed]:
        return Feed.query.get(feed_id)
    
    @staticmethod
    def create_feed(data: dict) -> Feed:
        feed = Feed(**data)
        db.session.add(feed)
        db.session.commit()
        return feed
    
    @staticmethod
    def update_feed(feed_id: int, data: dict) -> Optional[Feed]:
        feed = Feed.query.get(feed_id)
        if not feed:
            return None
        for key, value in data.items():
            setattr(feed, key, value)
        db.session.commit()
        return feed
    
    @staticmethod
    def delete_feed(feed_id: int) -> bool:
        feed = Feed.query.get(feed_id)
        if not feed:
            return False
        db.session.delete(feed)
        db.session.commit()
        return True