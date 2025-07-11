# tests/unit/utils/test_export_response.py

import pytest
from flask import Flask
from app.utils.export_response import (
    generate_export_response,
    generate_csv_response,
    generate_empty_csv_response
)
from app.utils.error_exceptions import ValidationError

app = Flask(__name__)

@pytest.fixture
def sample_data():
    return [
        {"name": "Podcast 1", "url": "http://example.com/1"},
        {"name": "Podcast 2", "url": "http://example.com/2"},
    ]

def test_generate_export_response_csv(sample_data):
    with app.test_request_context("/export?format=csv"):
        response = generate_export_response(sample_data, "feeds_export")
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/csv"
        assert "feeds_export.csv" in response.headers["Content-Disposition"]
        body = response.get_data(as_text=True)
        assert '"name","url"' in body
        assert "Podcast 1" in body

def test_generate_export_response_json(sample_data):
    with app.test_request_context("/export?format=json"):
        response = generate_export_response(sample_data, "feeds_export")
        assert response.status_code == 200
        assert response.is_json
        assert response.get_json()[0]["name"] == "Podcast 1"

def test_generate_export_response_empty_csv():
    with app.test_request_context("/export?format=csv"):
        response = generate_export_response([], "feeds_export")
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/csv"
        assert response.get_data(as_text=True) == ""

def test_generate_export_response_empty_json():
    with app.test_request_context("/export?format=json"):
        response = generate_export_response([], "feeds_export")
        assert response.status_code == 200
        assert response.get_json() == []

def test_generate_export_response_invalid_format():
    with app.test_request_context("/export?format=pdf"):
        with pytest.raises(ValidationError):
            generate_export_response([], "feeds_export")

def test_generate_csv_response(sample_data):
    headers = {"name": "name", "url": "url"}
    with app.test_request_context():
        response = generate_csv_response(sample_data, headers, "test.csv")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert '"name","url"' in body
        assert "Podcast 2" in body

def test_generate_empty_csv_response():
    with app.test_request_context():
        response = generate_empty_csv_response("empty.csv")
        assert response.status_code == 200
        assert response.get_data(as_text=True) == ""
        assert response.headers["Content-Disposition"] == "attachment; filename=empty.csv"
