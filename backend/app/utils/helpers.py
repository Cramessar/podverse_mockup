# app/utils/helpers.py

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

def is_auto_reparse_running() -> bool:
    """
    Check if the auto_reparse_all task is currently running.
    
    Returns:
        bool: True if auto_reparse_all is currently running, False otherwise
    """
    from app.utils.redis_lock import is_locked
    return is_locked("auto_reparse_all")