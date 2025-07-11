# tests/utils/test_request_logger.py

import pytest
from unittest.mock import MagicMock, patch
from flask import Flask, request, json
from app.utils.request_logger import log_request, log_database_operation

@pytest.fixture
def mock_logger():
    return MagicMock()

def test_log_request_basic(mock_logger):
    with Flask(__name__).test_request_context("/feeds", method="GET"):
        log_request(mock_logger, method="GET", resource="/feeds")
        mock_logger.info.assert_called_once()
        assert "GET /feeds" in mock_logger.info.call_args[0][0]

def test_log_request_with_payload(mock_logger):
    with Flask(__name__).test_request_context("/feeds", method="POST", json={"title": "Test Feed"}):
        with patch("app.utils.request_logger.truncate_payload", side_effect=lambda x, **kwargs: x):
            log_request(mock_logger, "POST", "/feeds", include_payload=True)
            args = mock_logger.info.call_args[0]
            assert "Payload" in args[0]
            assert "Test Feed" in args[0]

def test_log_request_payload_parse_fail(mock_logger):
    with Flask(__name__).test_request_context("/feeds", method="POST", data="bad_json"):
        log_request(mock_logger, "POST", "/feeds", include_payload=True)
        args = mock_logger.info.call_args[0]
        assert "unable to parse" in args[0]

def test_log_database_operation_with_id(mock_logger):
    log_database_operation(mock_logger, operation="UPDATE", table="feed", record_id=123)
    mock_logger.info.assert_called_once()
    assert "feed (ID: 123)" in mock_logger.info.call_args[0][0]

def test_log_database_operation_without_id(mock_logger):
    log_database_operation(mock_logger, operation="DELETE", table="channel")
    mock_logger.info.assert_called_once()
    assert "channel" in mock_logger.info.call_args[0][0]
    assert "(ID:" not in mock_logger.info.call_args[0][0]
