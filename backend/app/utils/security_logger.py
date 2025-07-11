# app/utils/security_logger.py

from flask import request, has_request_context
from typing import Optional, Union
from logging import Logger
from app.utils.log_config import get_audit_logger

def get_request_ip() -> Optional[str]:
    """Helper function to safely get request IP"""
    if has_request_context():
        return request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
    return None

def log_error(context: str, admin_id: str, error: Exception) -> None:
    """
    Helper function to log errors in consistent format with context and exception details across the codebase
    
    Args:
        context: Context of the error
        admin_id: User ID (required)
        error: Exception object
    """
    logger = get_audit_logger() # get the logger for the audit log
    logger.error(f"[ERROR] {context}: {str(error)} - User ID: {admin_id}", exc_info=True)


# for info
def log_auth_event(logger: Logger, event_type: str, admin_id: str, details: Optional[str] = None) -> None:
    """
    Helper function to log authentication events 
    
    Args:
        logger: Logger instance
        event_type: Type of auth event (LOGIN_SUCCESS, LOGIN_FAILED, LOGOUT, TOKEN_REFRESH, etc.)
        admin_id: User ID (required)
        details: Additional event details (optional)
    """
    log_msg = f"AUTH {event_type}"
    
    log_msg += f" - User ID: {admin_id}"
    if details:
        log_msg += f" - {details}"
    
    # Add IP address if available
    ip = get_request_ip()
    if ip:
        log_msg += f" - IP: {ip}"
    
    logger.info(log_msg)

# for watning 
def log_security_event(logger: Logger, event_type: str, admin_id: str, details: Optional[str] = None) -> None:
    """
    Helper function to log security-related events
    
    Args:
        logger: Logger instance
        admin_id: User ID (required)
        event_type: Type of security event (UNAUTHORIZED_ACCESS, RATE_LIMIT, etc.)
        details: Additional event details
    """
    log_msg = f"SECURITY {event_type}"
    
    log_msg += f" - User ID: {admin_id}"
    if details:
        log_msg += f" - {details}"
    
    # Add IP address if available
    ip = get_request_ip()
    if ip:
        log_msg += f" - IP: {ip}"
    
    logger.warning(log_msg)

# For warning 
def log_network_event(logger: Logger, event_type: str, admin_id: str, details: Optional[str] = None) -> None:
    """
    Helper function to log network related issues (timeouts, disconnects, etc)

    Args:
        logger: Logger instance
        event_type: Type of network issue (TIMEOUT, CONNECTION_ERROR, BROKENPIPE, etc)
        admin_id: User ID (required)
        details: Description or traceback
    """
    log_msg = f"NETWORK {event_type}"
    
    log_msg += f" - User ID: {admin_id}"
    if details:
        log_msg += f" - {details}"
    
    # Add client IP if available
    ip = get_request_ip()
    if ip:
        log_msg += f" - IP: {ip}"
    
    logger.warning(log_msg)


def log_admin_action(
    logger: Logger,
    admin_id: str,
    action: str,
    resource: str,
    resource_id: Union[str, int],
    details: Optional[str] = None
) -> None:
    """
    Logs administrative actions on resources (e.g., reparse, flag)

    Args:
        logger: Logger instance
        admin_id: ID of the admin user performing the action
        action: Type of action (e.g., REPARSE_FEED, FLAG_ITEM)
        resource: Type of resource (e.g., feed, item)
        resource_id: ID of the resource
        details: Optional context or route info
    """
    log_msg = f"ADMIN ACTION - {action} on {resource} (ID: {resource_id}) by User ID: {admin_id}"
    if details:
        log_msg += f" - {details}"

    ip = get_request_ip()
    if ip:
        log_msg += f" - IP: {ip}"

    logger.info(log_msg)
