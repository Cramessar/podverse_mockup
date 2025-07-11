# tests/utils/test_security_logger.py

import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from app.utils import security_logger

@pytest.fixture
def mock_logger():
    return MagicMock()

def test_get_request_ip():
    app = Flask(__name__)
    with app.test_request_context(headers={"X-Forwarded-For": "1.2.3.4"}):
        assert security_logger.get_request_ip() == "1.2.3.4"
        
def test_log_error(mock_logger):
    error = ValueError('Something broke')
    with patch("app.utils.security_logger.get_audit_logger", return_value=mock_logger):
        security_logger.log_error("test_context", "admin123", error) 
        mock_logger.error.assert_called_once()
        assert "test_context" in mock_logger.error.call_args[0][0]
        assert "Something broke" in mock_logger.error.call_args[0][0]

def test_log_auth_event_basic(mock_logger):
    security_logger.log_auth_event(mock_logger, event_type="LOGIN_SUCCESS", admin_id="admin123", details="Login via UI")
    mock_logger.info.assert_called_once()
    assert "LOGIN_SUCCESS" in mock_logger.info.call_args[0][0]
    assert "admin123" in mock_logger.info.call_args[0][0]
    
def test_log_security_event_warning(mock_logger):
    security_logger.log_security_event(mock_logger, event_type="UNAUTHORIZED_ACCESS", admin_id="admin123", details="Missing token")
    mock_logger.warning.assert_called_once()
    assert "UNAUTHORIZED_ACCESS" in mock_logger.warning.call_args[0][0]
    
def test_log_networking_event(mock_logger):
    security_logger.log_network_event(mock_logger, event_type="TIMEOUT", admin_id="admin123", details="API call timeout")
    mock_logger.warning.assert_called_once()
    assert "TIMEOUT" in mock_logger.warning.call_args[0][0]
    
def test_loh_admin_action(mock_logger):
    security_logger.log_admin_action(mock_logger, admin_id="admin123", action="REPARSE_FEED", resource="feed", resource_id=42, details="/feeds/42/reparse")
    mock_logger.info.assert_called_once()
    assert "REPARSE_FEED" in mock_logger.info.call_args[0][0]
    assert "42" in mock_logger.info.call_args[0][0]