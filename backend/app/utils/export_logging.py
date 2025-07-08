# backend/app/utils/export_logging.py

from app.models.export_logs import ExportLog
from app.extensions import db
from datetime import datetime
from app.blueprints.export_logs.schemas import export_log_schema

def create_export_log(data: dict) -> ExportLog:
    """ Creates and saves a new export log entry in the database when an export starts.
    
        Returns the created log entry.
    """
    log = ExportLog(**data)
    db.session.add(log)
    db.session.commit()
    return log

def finalize_export_log(log_id: int, status: str = None, file_path: str = None, format: str = None, 
                       feeds_count: int = None, error_message: str = None) -> ExportLog:
    """ Updates an existing log after the export finishes or fails.
    
        Returns the updated log entry.
    """
    log = ExportLog.query.get(log_id)
    if not log:
        return None
        
    if status:
        log.status = status
    if file_path:
        log.file_path = file_path
    if format:
        log.format = format
    if feeds_count is not None:
        log.feeds_count = feeds_count
    if error_message:
        log.error_message = error_message
        
    log.completed_at = datetime.utcnow()
    db.session.commit()
    return log

def create_export_log_simple(export_type: str, filters: dict = None, status: str = "pending", 
                           file_path: str = None, admin_email: str = "system@podverse.com") -> ExportLog:
    """ Creates a new export log entry with required fields.

        Returns:
            The created ExportLog instance.
    """
    data = {
        "admin_email": admin_email,
        "export_type": export_type,
        "filters": filters or {},
        "status": status,
        "file_path": file_path,
        "format": filters.get("format", "csv") if filters else "csv"
    }
    return create_export_log(data)