# backend/app/tasks/export_task.py

import os
from celery import shared_task
from celery.app.task import Task
from typing import Dict, Any
from app.services.data_export import export_data_to_csv
from app.utils.file_system_helpers import get_export_directory, FSError
from app.utils.redis_lock import redis_lock, RedisLockError
from app.utils.logger import get_logger

logger = get_logger(__name__)

@shared_task(bind=True, max_retries=3)
def scheduled_export_task(self: Task) -> Dict[str, Any]:
    """
    Scheduled task to export data to CSV files.
    Uses Redis lock to prevent multiple exports running simultaneously.
    Includes fallback to temp directory if primary export location is unavailable.
    """
    try:
        # Try to acquire Redis lock
        with redis_lock("scheduled_export", timeout=1800) as (acquired, error): # 30 minutes timeout
            if not acquired: # check teh state of lock
                logger.warning(f"Export task skipped: {error or 'lock not acquired'}")
                return {
                    "status": "skipped",
                    "reason": error or "already_running"
                }
            
            try:
                logger.info("Starting scheduled data export")
                
                # Get export directory with fallback
                primary_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'exports') 
                try:
                    export_dir, is_fallback = get_export_directory(primary_dir)
                    if is_fallback:
                        logger.warning("Using fallback export directory")
                except FSError as e:
                    logger.error(f"Failed to get export directory: {str(e)}")
                    raise
                
                # Perform export with directory override
                result = export_data_to_csv(export_dir=export_dir)
                
                logger.info(f"Export completed successfully: {result}")
                return {
                    "status": "success",
                    "result": result,
                    "using_fallback_directory": is_fallback
                }
                
            except FSError as e:
                logger.error(f"Filesystem error during export: {str(e)}")
                if self.request.retries < self.max_retries:
                    logger.info(f"Retrying export task (attempt {self.request.retries + 1})")
                    self.retry(exc=e, countdown=60 * (self.request.retries + 1))  # Exponential backoff
                return {
                    "status": "error",
                    "error": str(e)
                }
                
            except Exception as e:
                logger.error(f"Export failed: {str(e)}")
                if self.request.retries < self.max_retries: # if the task has not been retried 3 times
                    logger.info(f"Retrying export task (attempt {self.request.retries + 1})")
                    self.retry(exc=e, countdown=60 * (self.request.retries + 1))  # Exponential backoff
                return {
                    "status": "error",
                    "error": str(e)
                }
                
    except RedisLockError as e:
        logger.error(f"Redis lock error: {str(e)}")
        return {
            "status": "error",
            "error": f"Redis lock error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error in export task: {str(e)}")
        return {
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }
