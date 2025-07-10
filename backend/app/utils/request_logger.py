# app/utils/request_logger.py

import logging
import json
import time
from typing import Optional, Any, Dict, Union
from flask import request, g, Flask, Response
from logging import Logger
from app.utils.security_logger import log_security_event

def get_logger(name: str) -> Logger:
    """
    Get a logger with consistent formatting
    
    Args:
        name: Usually __name__ from the calling module
    
    Returns:
        Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only add handler if it doesn't already have one (prevents duplicates)
    if not logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # JSON structured formatter
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "message": "%(message)s"}'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        logger.setLevel(logging.INFO)
    
    return logger

def register_logging(app: Flask) -> None:
    """
    Register logging handlers for Flask app
    
    Args:
        app: Flask application instance
    """
    logger = get_logger(__name__)

    @app.before_request
    def before_request() -> None:
        log_request_start(logger)

    @app.after_request
    def after_request(response: Response) -> Response:
        return log_request_end(logger, response)

def log_request_start(logger: Logger) -> None:
    """
    Log incoming request details and start timer
    
    Args:
        logger: Logger instance
    """
    g.start_time = time.time()
    
    # Log the incoming request
    logger.info(f"REQUEST START: {request.method} {request.path}")
    
    # Log security-relevant headers
    user_agent = request.headers.get('User-Agent', 'Unknown')
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
    logger.info(f"REQUEST INFO: IP={ip}, User-Agent={user_agent[:100]}")
    
    # Check for potential security issues
    if len(request.path) > 1000:
        log_security_event(logger, 'SUSPICIOUS_REQUEST', details=f'Very long path: {len(request.path)} chars')
    
    # Log authentication header presence (without revealing token details)
    auth_header = request.headers.get('Authorization')
    if auth_header:
        logger.info(f"REQUEST AUTH: Authorization header present")
    else:
        logger.info(f"REQUEST AUTH: No authorization header")


def log_request_end(logger: Logger, response: Response) -> Response:
    """
    Log response details and completion time
    
    Args:
        logger: Logger instance
        response: Flask response object
    
    Returns:
        Response: The response object (for chaining)
    """
    total_time = time.time() - g.start_time if hasattr(g, 'start_time') else 0
    
    logger.info(f"RESPONSE: {request.method} {request.path} - {response.status_code} - {total_time:.3f}s")
    
    # Log error responses
    if response.status_code >= 400:
        logger.warning(f"ERROR RESPONSE: {request.method} {request.path} - {response.status_code}")
        
    # Log security events for suspicious status codes
    if response.status_code in [401, 403]:
        log_security_event(logger, 'ACCESS_DENIED', 
                         details=f'{request.method} {request.path} returned {response.status_code}')
    elif response.status_code == 429:
        log_security_event(logger, 'RATE_LIMIT_HIT', 
                         details=f'{request.method} {request.path}')
    
    return response



def log_request(logger: Logger, method: str, endpoint: str, 
               status_code: Optional[int] = None, include_payload: bool = False) -> None:
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

def log_database_operation(logger: Logger, operation: str, table: str, 
                         record_id: Optional[Union[int, str]] = None) -> None:
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
        
        

