"""
This module provides a minimal test environment for testing logging functionality
without requiring the full application context.
"""

import os
import logging
from flask import Flask

# Create logs directory if it doesn't exist
LOG_DIR = os.path.join(os.path.dirname(__file__), "test_logs")
os.makedirs(LOG_DIR, exist_ok=True)

def create_test_app():
    """Create a minimal Flask app for testing"""
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        'LOG_DIR': LOG_DIR
    })
    return app

def create_test_logger(name: str) -> logging.Logger:
    """Create a test logger that writes to a file in the test logs directory"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.FileHandler(os.path.join(LOG_DIR, f"{name}.log"))
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "message": "%(message)s"}'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger 