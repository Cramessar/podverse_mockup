import logging
import os
from logging.handlers import RotatingFileHandler

# Constants
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "security_audit.log")
MAX_PAYLOAD_LENGTH = 1000  # Maximum length for logged payloads
SENSITIVE_ROUTES = {"/login", "/register", "/auth", "/password-reset"}  # Routes where payload logging is forbidden
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with consistent formatting
    
    Args:
        name: Module name for the logger 
    
    Returns:
        Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "message": "%(message)s"}'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.setLevel(logging.INFO)
    
    return logger

def get_audit_logger() -> logging.Logger:
    """
    Get the audit logger with file rotation
    
    Returns:
        Logger: Configured audit logger instance
    """
    logger = logging.getLogger("audit_logger")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        file_handler = RotatingFileHandler( # rotates/ creates a new file when the old one is too large then deletes the old one when number of backups is reached
            LOG_FILE, maxBytes=5*1024*1024, backupCount=3
        )
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "message": %(message)s}'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


# 
def truncate_payload(payload: dict, max_length: int = MAX_PAYLOAD_LENGTH) -> dict:
    """
    shorten the data(payload) from request/response before logging it to prevent log bloat or sensitive data exposure
    
    Args:
        payload: Dictionary to truncate
        max_length: Maximum length for string values
        
    Returns:
        dict: Truncated payload
    """
    truncated = {}
    for key, value in payload.items():
        if isinstance(value, str) and len(value) > max_length:
            truncated[key] = value[:max_length] + "..."
        elif isinstance(value, dict):
            truncated[key] = truncate_payload(value, max_length)
        else:
            truncated[key] = value
    return truncated 