# app/utils/request_logger.py

import json
import time
from typing import Optional, Union
from flask import request, g, Flask, Response, has_request_context
from logging import Logger
from app.utils.log_config import get_logger, truncate_payload

def register_logging(app: Flask) -> None:
    """
    Register logging handlers for Flask app
    
    Args:
        app: Flask application instance
    """
    logger = get_logger(__name__)

    @app.before_request # logs method, path, headers, maybe payload start time
    def before_request() -> None:
        log_request_start(logger)

    @app.after_request # logs response status, duration, maybe response body
    def after_request(response: Response) -> Response:
        return log_request_end(logger, response)

def log_request_start(logger: Logger) -> None:
    """
    Log incoming request details and start timer
    
    Args:
        logger: Logger instance
    """
    g.start_time = time.time() # stores request start time to use later measure request duration
    
    # Log the incoming request
    logger.info(f"REQUEST START: {request.method} {request.path}")
    
    # Log security-relevant headers if in request context
    if has_request_context():
        user_agent = request.headers.get('User-Agent', 'Unknown') # rate limiting, bot detection
        ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
        logger.info(f"REQUEST INFO: IP={ip}, User-Agent={user_agent[:100]}")
        
        # for potential security issues 
        if len(request.path) > 1000:
            from app.utils.security_logger import log_security_event
            log_security_event(logger, 'SUSPICIOUS_REQUEST', details=f'Very long path: {len(request.path)} chars')
        
        # log authentication header  (without revealing token details)
        auth_header = request.headers.get('Authorization')
        if auth_header:
            logger.info(f"REQUEST AUTH: Authorization header present")
        else:
            logger.info(f"REQUEST AUTH: No authorization header")


def log_request_end(logger: Logger, response: Response) -> Response:
    """
    Log response details like how the request ended—status code, time taken, and any errors or security-related issues.
    
    Args:
        logger: Logger instance
        response: Flask response object
    
    Returns:
        Response: The response object (for chaining)
    """
    if has_request_context():
        total_time = time.time() - g.start_time if hasattr(g, 'start_time') else 0 # in seconds (float)
        
        logger.info(f"RESPONSE: {request.method} {request.path} - {response.status_code} - {total_time:.3f}s")
        
        # Log error responses
        if response.status_code >= 400:
            logger.warning(f"ERROR RESPONSE: {request.method} {request.path} - {response.status_code}")
            
        # Log security events for suspicious status codes
        if response.status_code in [401, 403]:
            from app.utils.security_logger import log_security_event
            log_security_event(logger, 'ACCESS_DENIED', 
                            details=f'{request.method} {request.path} returned {response.status_code}')
        elif response.status_code == 429:
            from app.utils.security_logger import log_security_event
            log_security_event(logger, 'RATE_LIMIT_HIT', 
                            details=f'{request.method} {request.path}')
    
    return response

def log_request(logger: Logger, method: str, resource: str, 
               status_code: Optional[int] = None, include_payload: bool = False) -> None:
    """
    Helper function to log HTTP requests consistently
    
    Args:
        logger: Logger instance
        method: HTTP method (GET, POST, etc.)
        resource: API resource
        status_code: HTTP status code (optional)
        include_payload: Whether to log request payload (for sensitive routes)
    """
    log_msg = f"{method} {resource}"
    
    if include_payload and has_request_context():
        # skip payload logging for sensitive routes
        if request.path:
            try:
                payload = request.get_json()
                safe_payload = truncate_payload(payload)
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
        
        

