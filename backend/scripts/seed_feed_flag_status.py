from seed_utils import get_db_session
from app.models.feed import FeedFlagStatus
from sqlalchemy.exc import IntegrityError

feed_flag_statuses = [
    "active",
    "always-parse",
    "spam",
    "pending-archive",
    "archived",
    "takedown"
]

def seed_feed_flag_status():
    session = get_db_session()
    try:
        for status in feed_flag_statuses:
            entry = FeedFlagStatus(status=status)
            session.add(entry)
        session.commit()
        print("✅ Feed flag statuses seeded successfully")
    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_feed_flag_status()
