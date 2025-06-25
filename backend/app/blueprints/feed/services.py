# feed_service.py

#NOT: Refactor into classes only if logic grows more complex for now stand alonw functions are already modular since it's in the same file

from app.models.feed import Feed
from app.extensions import db
from app.utils.logger import get_logger, log_request, log_database_operation
from sqlalchemy import select

logger = get_logger(__name__)

class DuplicateFeedError(Exception):
    pass

def create_feed_service(feed_data):  # Creates a new feed from validated input
    # feed_data is already a Feed instance from marshmallow schema
    query = select(Feed).where(Feed.url == feed_data.url)
    existing_feed = db.session.execute(query).scalar_one_or_none() # Check if feed with same URL already exists
    if existing_feed:
        raise DuplicateFeedError("Feed with this URL already exists")  # Prevent inserting duplicates
    
    db.session.add(feed_data)      # Add the new feed to the session
    db.session.commit()           # Commit the transaction to save it
    return feed_data              # Return the newly created feed
    
