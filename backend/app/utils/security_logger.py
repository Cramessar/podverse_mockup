# app/utils/security_logger.py

from flask import request
from typing import Optional, Dict, Any, Union
from logging import Logger
from app.utils.request_logger import get_logger

def log_auth_event(logger: Logger, event_type: str, user_id: Optional[str] = None, 
                  email: Optional[str] = None, details: Optional[str] = None) -> None:
    """
    Helper function to log authentication events
    
    Args:
        logger: Logger instance
        event_type: Type of auth event (LOGIN_SUCCESS, LOGIN_FAILED, LOGOUT, TOKEN_REFRESH, etc.)
        user_id: User ID (optional)
        email: User email (optional)
        details: Additional event details (optional)
    """
    log_msg = f"AUTH {event_type}"
    
    if user_id:
        log_msg += f" - User ID: {user_id}"
    if email:
        log_msg += f" - Email: {email}"
    if details:
        log_msg += f" - {details}"
    
    # Add IP address if available
    if request:
        ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
        if ip:
            log_msg += f" - IP: {ip}"
    
    logger.info(log_msg)
    
    

def log_security_event(logger: Logger, event_type: str, details: Optional[str] = None) -> None:
    """
    Helper function to log security-related events
    
    Args:
        logger: Logger instance
        event_type: Type of security event (UNAUTHORIZED_ACCESS, RATE_LIMIT, etc.)
        details: Additional event details
    """
    log_msg = f"SECURITY {event_type}"
    
    if details:
        log_msg += f" - {details}"
    
    # Add IP address if available
    if request:
        ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
        if ip:
            log_msg += f" - IP: {ip}"
    
    logger.warning(log_msg)
    
    

def log_network_event(logger: Logger, event_type: str, details: Optional[str] = None) -> None:
    """
    Helper function to log network related issues (timeouts, disconnects, etc)

    Args:
        logger: Logger instance
        event_type: Type of network issue (TIMEOUT, CONNECTION_ERROR, BROKENPIPE, etc)
        details: Description or traceback
    """
    log_msg = f"NETWORK {event_type}"

    if details:
        log_msg += f" - {details}"
    
    # Add client IP if available
    if request:
        ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
        if ip:
            log_msg += f" - IP: {ip}"
    
    logger.warning(log_msg)
    
    
    
def log_error(context: str, error: Exception) -> None:
    """
    Helper function to log errors in consistent format with context and exception details across the codebase
    
    Args:
        context: Context of the error
        error: Exception object
    """
    logger = get_logger(context)
    logger.error(f"[ERROR] {context}: {str(error)}", exc_info=True)
  
  
    
# all /admin/* actions
from typing import Optional, Union
from flask import request
from logging import Logger

def log_admin_action(
    logger: Logger,
    user_id: str,
    action: str,
    resource: str,
    resource_id: Union[str, int],
    details: Optional[str] = None
) -> None:
    """
    Logs administrative actions on resources (e.g., reparse, flag)

    Args:
        logger: Logger instance
        user_id: ID of the admin user performing the action
        action: Type of action (e.g., REPARSE_FEED, FLAG_ITEM)
        resource: Type of resource (e.g., feed, item)
        resource_id: ID of the resource
        details: Optional context or route info
    """
    log_msg = f"ADMIN ACTION - {action} on {resource} (ID: {resource_id}) by User ID: {user_id}"
    if details:
        log_msg += f" - {details}"

    if request:
        ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
        if ip:
            log_msg += f" - IP: {ip}"

    logger.info(log_msg)




# export or download endpoints
def log_data_export(logger: Logger, user_id: str, endpoint: str, filters: Optional[Dict[str, Any]] = None) -> None:
    """
    Logs bulk data export actions for audit tracking

    Args:
        logger: Logger instance
        user_id: ID of the user performing the export
        endpoint: API route or function used for export
        filters: Applied filters (non-sensitive only)
    """
    log_msg = f"EXPORT - User ID: {user_id} - Endpoint: {endpoint}"
    if filters:
        log_msg += f" - Filters: {filters}"
    
    if request:
        ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
        if ip:
            log_msg += f" - IP: {ip}"
    
    logger.info(log_msg)
    
    
 # when done wirh tabel - handler = logging.FileHandler("security_audit.log")
# handler.setFormatter(...)
# logger.addHandler(handler)