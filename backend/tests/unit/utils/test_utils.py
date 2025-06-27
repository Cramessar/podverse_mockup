import pytest
from unittest.mock import patch
import io
from flask import Flask

from app.utils.cvs_response import generate_csv_response


class TestCSVUtils:
    """Test CSV utility functions."""
    
    def test_generate_csv_response_with_data(self):
        """Test CSV generation with valid data."""
        data = [
            {'id': 1, 'name': 'Test 1', 'value': 'A'},
            {'id': 2, 'name': 'Test 2', 'value': 'B'}
        ]
        filename = 'test_export.csv'
        
        with Flask(__name__).app_context():
            response = generate_csv_response(data, filename)
        
        # Check response properties
        assert response.status_code == 200
        assert response.mimetype == 'text/csv'
        assert 'Content-Disposition' in response.headers
        assert f'attachment; filename="{filename}"' in response.headers['Content-Disposition']
        
        # Check CSV content
        csv_content = response.get_data(as_text=True)
        lines = [line.strip() for line in csv_content.strip().split('\n')]
        
        # Should have header + 2 data rows
        assert len(lines) == 3
        
        # Check header
        assert 'id,name,value' == lines[0]
        
        # Check data rows
        assert '1,Test 1,A' == lines[1]
        assert '2,Test 2,B' == lines[2]
    
    def test_generate_csv_response_empty_data(self):
        """Test CSV generation with empty data."""
        data = []
        filename = 'empty_export.csv'
        
        with Flask(__name__).app_context():
            response = generate_csv_response(data, filename)
        
        # Check response properties
        assert response.status_code == 200
        assert response.mimetype == 'text/csv'
        assert 'Content-Disposition' in response.headers
        assert f'attachment; filename="{filename}"' in response.headers['Content-Disposition']
        
        # Check CSV content is empty
        csv_content = response.get_data(as_text=True)
        assert csv_content == ''
    
    def test_generate_csv_response_with_special_characters(self):
        """Test CSV generation with special characters that need escaping."""
        data = [
            {'id': 1, 'name': 'Test, with comma', 'description': 'Test "with quotes"'},
            {'id': 2, 'name': 'Test\nwith newline', 'description': 'Normal text'}
        ]
        filename = 'special_chars_export.csv'
        
        with Flask(__name__).app_context():
            response = generate_csv_response(data, filename)
        
        # Check response properties
        assert response.status_code == 200
        assert response.mimetype == 'text/csv'
        
        # Check CSV content handles special characters
        csv_content = response.get_data(as_text=True)
        lines = [line.strip() for line in csv_content.strip().split('\n')]
        
        # Should have header + 2 data rows (though newlines might create additional lines)
        assert len(lines) >= 3
        
        # Check that commas and quotes are properly handled in CSV
        assert 'id,name,description' == lines[0]
        # The CSV writer should properly escape the comma and quotes
        assert '"Test, with comma"' in csv_content
        assert '"""Test ""with quotes"""""' in csv_content or '"Test ""with quotes"""' in csv_content
    
    def test_generate_csv_response_with_none_values(self):
        """Test CSV generation with None values."""
        data = [
            {'id': 1, 'name': 'Test 1', 'value': None},
            {'id': 2, 'name': None, 'value': 'B'}
        ]
        filename = 'none_values_export.csv'
        
        with Flask(__name__).app_context():
            response = generate_csv_response(data, filename)
        
        # Check response properties
        assert response.status_code == 200
        assert response.mimetype == 'text/csv'
        
        # Check CSV content
        csv_content = response.get_data(as_text=True)
        lines = [line.strip() for line in csv_content.strip().split('\n')]
        
        # Should have header + 2 data rows
        assert len(lines) == 3
        
        # Check header
        assert 'id,name,value' == lines[0]
        
        # Check that None values are represented as empty strings
        assert '1,Test 1,' == lines[1]
        assert '2,,B' == lines[2]
    
    def test_generate_csv_response_filename_security(self):
        """Test that filename is properly set in headers."""
        data = [{'id': 1, 'name': 'Test'}]
        # Test with potentially problematic filename
        filename = 'test"file<name>.csv'
        
        with Flask(__name__).app_context():
            response = generate_csv_response(data, filename)
        
        # Check that filename is included (browser will handle security)
        assert 'Content-Disposition' in response.headers
        assert filename in response.headers['Content-Disposition'] 