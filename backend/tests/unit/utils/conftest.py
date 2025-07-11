import os
import sys
import pytest
from flask import Flask

# Add the backend directory to Python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
    })
    
    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner() 