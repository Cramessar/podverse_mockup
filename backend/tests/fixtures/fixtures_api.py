import pytest
from flask import url_for

@pytest.fixture
def api_client(app):
    """Create a test client for API testing."""
    return app.test_client()

@pytest.fixture
def api_headers():
    """Default headers for API requests."""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    } 