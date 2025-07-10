from seed_utils import get_db_session
from app.models.feed import FeedFlagStatus
from sqlalchemy.exc import IntegrityError
from backend.app.utils.request_logger import get_logger

logger = get_logger(__name__)

feed_flag_statuses = [
    "active",
    "always-parse",
    "spam",
    "pending-archive",
    "archived",
    "takedown",
    "parse_error",
    "fetch_error"
]

def seed_feed_flag_status():
    session = get_db_session()
    try:
        for status in feed_flag_statuses:
            # Check if status exists
            existing = session.query(FeedFlagStatus).filter_by(status=status).first()
            if not existing:
                entry = FeedFlagStatus(status=status)
                session.add(entry)
                logger.info(f"Added new status: {status}")
            else:
                logger.info(f"Status already exists: {status}")
        session.commit()
        logger.info("Feed flag statuses seeded successfully")
    except Exception as e:
        session.rollback()
        logger.error(f"Error seeding feed flag statuses: {str(e)}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    seed_feed_flag_status()
