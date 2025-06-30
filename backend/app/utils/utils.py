#app/utils/utils.py

from app.extensions import db

def get_flag_status_id(status: str) -> int:
    """
    Get the ID of a feed flag status by its status string.
    """
    from app.models.feed import FeedFlagStatus
    record = db.session.query(FeedFlagStatus).filter_by(status=status).first()
    if not record:
        raise RuntimeError(f"FeedFlagStatus '{status}' not found")
    return record.id