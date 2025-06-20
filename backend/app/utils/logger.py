import logging
import os
import json
from flask import request

def get_logger(name):
    """
    Get a logger with consistent formatting
    
    Args:
        name: Usually __name__ from the calling module
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only add handler if it doesn't already have one (prevents duplicates)
    if not logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
        logger.setLevel(logging.INFO)
    
    return logger

def log_request(logger, method, endpoint, status_code=None, include_payload=False):
    """
    Helper function to log HTTP requests consistently
    
    Args:
        logger: Logger instance
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint
        status_code: HTTP status code (optional)
        include_payload: Whether to log request payload (for sensitive routes)
    """
    log_msg = f"{method} {endpoint}"
    
    if include_payload and request.is_json:
        try:
            payload = request.get_json()
            # Don't log sensitive fields
            safe_payload = {k: v for k, v in payload.items() 
                          if k not in ['password', 'token', 'secret', 'key']}
            log_msg += f" - Payload: {json.dumps(safe_payload)}"
        except Exception:
            log_msg += " - Payload: [unable to parse]"
    
    if status_code:
        log_msg += f" - {status_code}"
    
    logger.info(log_msg)

def log_database_operation(logger, operation, table, record_id=None):
    """
    Helper function to log database operations
    
    Args:
        logger: Logger instance
        operation: Type of operation (CREATE, READ, UPDATE, DELETE)
        table: Database table name
        record_id: Record ID (optional)
    """
    if record_id:
        logger.info(f"DB {operation}: {table} (ID: {record_id})")
    else:
        logger.info(f"DB {operation}: {table}")

def log_auth_event(logger, event_type, user_id=None, email=None, details=None):
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

def log_security_event(logger, event_type, details=None):
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