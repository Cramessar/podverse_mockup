# tests/unit/utils/test_audit_decorators.py

import pytest
from flask import Flask, request
from unittest.mock import patch, MagicMock
from app.utils.audit_decorators import audit_admin_access

app = Flask(__name__)

@audit_admin_access(action="REPARSE_FEED", resource="feed")
def sample_view(id):
    return f"Feed {id} reparsed"

def test_audit_admin_access_logs_correctly():
    mock_logger = MagicMock()

    with app.test_request_context("/feeds/123/reparse", method="POST"):
        # Simulate request.admin with a .sub property
        request.admin = MagicMock(sub="admin456")

        with patch("app.utils.audit_decorators.get_audit_logger", return_value=mock_logger), \
             patch("app.utils.audit_decorators.log_admin_action") as mock_log_action:
            
            result = sample_view(id=123)

            # Verify the decorated function returns expected result
            assert result == "Feed 123 reparsed"

            # log_admin_action should be called once with correct values
            mock_log_action.assert_called_once()
            args, kwargs = mock_log_action.call_args

            assert kwargs["admin_id"] == "admin456"
            assert kwargs["action"] == "REPARSE_FEED"
            assert kwargs["resource"] == "feed"
            assert kwargs["resource_id"] == 123
            assert "POST /feeds/123/reparse" in kwargs["details"]
