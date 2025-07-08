# backend/app/tasks/export_task.py

import os
from celery import shared_task
from celery.app.task import Task
from typing import Dict, Any
from app.services.data_export import export_data_to_csv
from app.utils.file_system_helpers import get_export_directory, FSError
from app.utils.redis_lock import redis_lock, RedisLockError
from app.utils.logger import get_logger, log_error
from datetime import datetime, timedelta
from app.extensions import db
from app.models.export_logs import ExportLog
from app.utils.export_logging import create_export_log_simple, finalize_export_log


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
                
                # Create export log
                log = create_export_log_simple(
                    export_type="channels",
                    format="csv",
                    filters={} # no filters for scheduled export
                )
                
                # Perform export with directory override
                result = export_data_to_csv(export_dir=export_dir)
                
                # finalize export log
                finalize_export_log(
                    log, 
                    status="success" , 
                    file_path=os.path.join(result["export_directory"], result["channels_file"]), 
                    counts={
                        "channels": result.get("channels_count", 0),
                        "feeds": result.get("feeds_count", 0),
                        "items": result.get("items_count", 0)
                    }
                )
                
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
                    finalize_export_log(log, status="failed", error_message=str(e))
                    # retry the task
                    self.retry(exc=e, countdown=60 * (self.request.retries + 1))  # exponential backoff
                return {
                    "status": "error",
                    "error": str(e)
                }
                
            except Exception as e:
                logger.error(f"Export failed: {str(e)}")
                if self.request.retries < self.max_retries: # if the task has not been retried 3 times
                    logger.info(f"Retrying export task (attempt {self.request.retries + 1})")
                    finalize_export_log(log, status="failed", error_message=str(e))
                    
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

@shared_task
def cleanup_old_export_files() -> str:
    """
    Cleanup export files older than 30 days and update their records.
    """
    # Find logs with files older than 30 days #! this can be increased 
    cutoff_date = datetime.utcnow() - timedelta(days=30) # delete files older than 30 days
    old_logs = ExportLog.query.filter(ExportLog.created_at < cutoff_date, ExportLog.file_path.isnot(None)).all() # get logs with files older than 30 days

    for log in old_logs:
        if log.file_path and os.path.exists(log.file_path):
            try:
                os.remove(log.file_path) # if os remove fails continue with other files
            except OSError:
                # Log error but continue with other files
                log_error(f"Failed to delete export file: {log.file_path}")
                continue
        
        # Update log record
        log.file_path = None
        log.status = "expired"
        if not log.completed_at:
            log.completed_at = datetime.utcnow()
    try:
        db.session.commit()
    except Exception as e:
        log_error(f"DB commit failed during export cleanup: {str(e)}")
        raise

    logger.info(f"Cleanup complete. Processed {len(old_logs)} old export files.")
    return f"Processed {len(old_logs)} old export files"

#TODO: refactor cleanup_old_export_files task and config etc after dedcinding where to store the files 