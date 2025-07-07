# app/tasks/feed_task.py

from celery import shared_task
from celery.app.task import Task
from typing import Dict, List, Any
from app.extensions import db
from app.models import Feed
from app.blueprints.feed.services import parse_and_update_feed_object
from app.utils.error_exceptions import NotFoundError
from app.utils.helpers import get_flag_status_id
from app.utils.redis_lock import redis_lock
from app.utils.logger import get_logger
from datetime import datetime, timedelta
from sqlalchemy import and_

logger = get_logger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)  # 60 seconds between retries, 3 retries max
def reparse_feed_task(self: Task, feed_id: int) -> Dict[str, int]:
    """
    Celery task to reparse a single feed.
    
    Args:
        self: Celery task instance
        feed_id: ID of the feed to reparse
        
    Returns:
        Dict[str, int]: Dictionary containing number of feeds reparsed
        
    Raises:
        NotFoundError: If feed with given ID doesn't exist
    """
    try:
        # call parse and update feed object in task wrapper so celery can queue and run it
        feed = db.session.get(Feed, feed_id)
        if not feed:
            raise NotFoundError(f"Feed with ID {feed_id} not found")
        return parse_and_update_feed_object(feed)
    except NotFoundError:
        self.retry(exc=NotFoundError)
    except Exception as e:
        self.retry(exc=e)
    return {"reparsed": 1}


@shared_task
def auto_reparse_all() -> Dict[str, Any]:
    """
    Reparse all feeds that have been updated in the last hour that are in the parse_error, fetch_error, or always-parse status.
    Uses Redis lock to prevent multiple instances running simultaneously.
    
    Returns:
        Dict[str, Any]: Dictionary containing:
            - reparsed (int): Number of feeds queued for reparse
            - skipped (bool): Whether execution was skipped due to lock
            - queued_feed_ids (List[int]): IDs of successfully queued feeds
            - error_feed_ids (List[int]): IDs of feeds that failed to queue
    """
    with redis_lock("auto_reparse_all", timeout=600) as (acquired, error):  # 10 minute timeout
        if not acquired:
            logger.warning("auto_reparse_all already running, skipping this execution")
            return {
                "reparsed": 0, 
                "skipped": True, 
                "reason": "already_running",
                "queued_feed_ids": [],
                "error_feed_ids": []
            }
        
        logger.info("Starting auto_reparse_all with Redis lock acquired")
        
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)

        feeds = db.session.query(Feed).filter(
            and_(
                Feed.feed_flag_status_id.in_([
                    get_flag_status_id("parse_error"),
                    get_flag_status_id("fetch_error"),
                    get_flag_status_id("always-parse")
                ]),
                Feed.updated_at < one_hour_ago,
                Feed.is_parsing == False
            )
        ).limit(50)

        count: int = 0
        queued_feed_ids: List[int] = []
        error_feed_ids: List[int] = []

        for feed in feeds:
            try:
                reparse_feed_task.delay(feed.id)  # fire async
                queued_feed_ids.append(feed.id) # add to list of queued feed ids to see which seed were successfilo or unsecc procssed during each batch
                count += 1
                logger.info(f"Queued feed ID {feed.id} for reparse (status: {feed.feed_flag_status.status})")
            except Exception as e:
                error_feed_ids.append(feed.id)
                logger.error(f"Failed to queue reparse for feed {feed.id}: {str(e)}")
                db.session.rollback()
        
        # Log summary with structured data
        logger.info(
            "auto_reparse_all completed",
            extra={
                "queued_count": count,
                "queued_feed_ids": queued_feed_ids,
                "error_feed_ids": error_feed_ids,
                "execution_time": datetime.utcnow().isoformat()
            }
        )
        return {
            "reparsed": count,
            "skipped": False,
            "queued_feed_ids": queued_feed_ids,
            "error_feed_ids": error_feed_ids
        }

