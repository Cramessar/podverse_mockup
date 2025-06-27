import pytest
from unittest.mock import patch, MagicMock
from flask import json
import time

from app.utils.auth import AuthError
from app.utils.error_exceptions import ValidationError, NotFoundError, DatabaseError


class TestChannelRoutes:
    """Test the channel routes and their functionality."""
    
    @pytest.fixture
    def client(self, app):
        """Create a test client for the Flask application."""
        return app.test_client()
    
    @pytest.fixture
    def auth_headers(self):
        """Mock authorization headers for testing."""
        return {'Authorization': 'Bearer valid.jwt.token'}
    
    @pytest.fixture
    def mock_auth_success(self):
        """Mock successful authentication."""
        with patch('app.blueprints.channel.routes.requires_auth') as mock_auth:
            def decorator(f):
                return f
            mock_auth.return_value = decorator
            yield mock_auth
    
    def test_get_all_channels_success(self, client, auth_headers, mock_auth_success):
        """Test successful retrieval of all channels."""
        mock_channels_data = [
            {'id': 1, 'title': 'Test Channel 1', 'description': 'Test Description 1'},
            {'id': 2, 'title': 'Test Channel 2', 'description': 'Test Description 2'}
        ]
        
        with patch('app.blueprints.channel.routes.list_channels') as mock_list:
            mock_list.return_value = {
                "data": mock_channels_data,
                "meta": {"total": 2, "limit": 10, "offset": 0}
            }
            
            response = client.get('/channels', headers=auth_headers)
            
        assert response.status_code == 200
        mock_list.assert_called_once()
    
    def test_get_all_channels_without_auth(self, client):
        """Test that accessing channels without auth returns 401."""
        with patch('app.utils.auth.get_token_auth_header') as mock_get_token:
            mock_get_token.side_effect = AuthError({"code": "authorization_header_missing"}, 401)
            
            response = client.get('/channels')
            
        assert response.status_code == 401
    
    def test_export_channels_success(self, client, auth_headers, mock_auth_success):
        """Test successful export of channels as CSV."""
        with patch('app.blueprints.channel.routes.export_channels') as mock_export:
            mock_export.return_value = MagicMock(
                status_code=200,
                headers={'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename="channels_export_20240101_120000.csv"'},
                data=b'id,title,medium_name\n1,Test Channel,podcast\n'
            )
            
            response = client.get('/channels/export', headers=auth_headers)
            
        assert response.status_code == 200
        mock_export.assert_called_once()
    
    def test_export_channels_with_filters(self, client, auth_headers, mock_auth_success):
        """Test export with query parameters."""
        with patch('app.blueprints.channel.routes.export_channels') as mock_export:
            mock_export.return_value = MagicMock(status_code=200)
            
            response = client.get('/channels/export?search=test&sort_by=title&sort_order=desc&max_rows=5000', headers=auth_headers)
            
        assert response.status_code == 200
        mock_export.assert_called_once()
    
    def test_export_channels_without_auth(self, client):
        """Test that accessing export without auth returns 401."""
        with patch('app.utils.auth.get_token_auth_header') as mock_get_token:
            mock_get_token.side_effect = AuthError({"code": "authorization_header_missing"}, 401)
            
            response = client.get('/channels/export')
            
        assert response.status_code == 401
    
    def test_get_single_channel_success(self, client, auth_headers, mock_auth_success):
        """Test successful retrieval of a single channel."""
        mock_channel_data = {
            'id': 1, 
            'title': 'Test Channel', 
            'description': 'Test Description'
        }
        
        with patch('app.blueprints.channel.routes.get_channel_by_id') as mock_get:
            mock_get.return_value = {"data": mock_channel_data}
            
            response = client.get('/channels/1', headers=auth_headers)
            
        assert response.status_code == 200
        mock_get.assert_called_once_with(1)
    
    def test_get_single_channel_not_found(self, client, auth_headers, mock_auth_success):
        """Test retrieval of non-existent channel returns 404."""
        with patch('app.blueprints.channel.routes.get_channel_by_id') as mock_get:
            mock_get.side_effect = NotFoundError("Channel not found")
            
            response = client.get('/channels/999', headers=auth_headers)
            
        assert response.status_code == 404
    
    def test_get_single_channel_invalid_id(self, client, auth_headers, mock_auth_success):
        """Test retrieval with invalid channel ID returns 400."""
        with patch('app.blueprints.channel.routes.get_channel_by_id') as mock_get:
            mock_get.side_effect = ValidationError("Invalid channel ID")
            
            response = client.get('/channels/invalid', headers=auth_headers)
            
        assert response.status_code == 400
    
    def test_get_single_channel_database_error(self, client, auth_headers, mock_auth_success):
        """Test database error handling returns 500."""
        with patch('app.blueprints.channel.routes.get_channel_by_id') as mock_get:
            mock_get.side_effect = DatabaseError("Database connection failed")
            
            response = client.get('/channels/1', headers=auth_headers)
            
        assert response.status_code == 500


class TestChannelExportController:
    """Test the channel export controller functionality."""
    
    @pytest.fixture
    def mock_channel(self):
        """Create a mock channel object."""
        mock_channel = MagicMock()
        mock_channel.id = 1
        mock_channel.id_text = "abc123"
        mock_channel.title = "Test Channel"
        mock_channel.sortable_title = "test channel"
        mock_channel.slug = "test-channel"
        mock_channel.podcast_index_id = 12345
        mock_channel.podcast_guid = "guid-123"
        mock_channel.has_podcast_index_value = True
        mock_channel.has_value_time_splits = False
        mock_channel.created_at = None
        mock_channel.updated_at = None
        mock_channel.medium_id = 1
        mock_channel.medium.name = "podcast"
        mock_channel.feed_id = 1
        mock_channel.feed.url = "https://example.com/feed.xml"
        mock_channel.feed.status = "active"
        mock_channel.stats = [MagicMock(
            all_time_count=100,
            month_current_count=20,
            week_current_count=5,
            day_current_count=1
        )]
        return mock_channel
    
    @patch('app.blueprints.channel.controller.get_channels_for_export')
    @patch('app.blueprints.channel.controller.get_sorting_params')
    @patch('app.blueprints.channel.controller.get_search_query')
    @patch('app.blueprints.channel.controller.generate_csv_response')
    def test_export_channels_controller_success(self, mock_csv_response, mock_search, mock_sorting, mock_get_channels, mock_channel):
        """Test successful export via controller."""
        from app.blueprints.channel.controller import export_channels
        from flask import Flask
        
        # Setup mocks
        mock_search.return_value = None
        mock_sorting.return_value = ('id', 'asc')
        mock_get_channels.return_value = [mock_channel]
        mock_csv_response.return_value = MagicMock(status_code=200)
        
        with Flask(__name__).test_request_context():
            result = export_channels()
        
        # Verify calls
        mock_get_channels.assert_called_once_with(None, 'id', 'asc', 10000)
        mock_csv_response.assert_called_once()
        
        # Check CSV data structure
        call_args = mock_csv_response.call_args[0]
        export_data = call_args[0]
        filename = call_args[1]
        
        assert len(export_data) == 1
        assert export_data[0]['id'] == 1
        assert export_data[0]['title'] == "Test Channel"
        assert export_data[0]['medium_name'] == "podcast"
        assert 'channels_export_' in filename
        assert filename.endswith('.csv')
    
    @patch('app.blueprints.channel.controller.get_channels_for_export')
    @patch('app.blueprints.channel.controller.get_sorting_params')
    @patch('app.blueprints.channel.controller.get_search_query')
    @patch('app.blueprints.channel.controller.generate_csv_response')
    def test_export_channels_with_search(self, mock_csv_response, mock_search, mock_sorting, mock_get_channels):
        """Test export with search filter."""
        from app.blueprints.channel.controller import export_channels
        from flask import Flask
        
        # Setup mocks
        mock_search.return_value = "test"
        mock_sorting.return_value = ('title', 'desc')
        mock_get_channels.return_value = []
        mock_csv_response.return_value = MagicMock(status_code=200)
        
        with Flask(__name__).test_request_context():
            result = export_channels()
        
        mock_get_channels.assert_called_once_with("test", 'title', 'desc', 10000)
    
    @patch('app.blueprints.channel.controller.get_channels_for_export')
    @patch('app.blueprints.channel.controller.get_sorting_params')
    @patch('app.blueprints.channel.controller.get_search_query')
    def test_export_channels_database_error(self, mock_search, mock_sorting, mock_get_channels):
        """Test export with database error."""
        from app.blueprints.channel.controller import export_channels
        from flask import Flask
        
        # Setup mocks
        mock_search.return_value = None
        mock_sorting.return_value = ('id', 'asc')
        mock_get_channels.side_effect = Exception("Database error")
        
        with Flask(__name__).test_request_context():
            with pytest.raises(DatabaseError, match="Failed to export channels"):
                export_channels()


class TestChannelRateLimiting:
    """Test rate limiting functionality for channel endpoints."""
    
    @pytest.fixture
    def client(self, app):
        """Create a test client for the Flask application."""
        return app.test_client()
    
    @pytest.fixture
    def auth_headers(self):
        """Mock authorization headers for testing."""
        return {'Authorization': 'Bearer valid.jwt.token'}
    
    @pytest.fixture
    def mock_auth_success(self):
        """Mock successful authentication."""
        with patch('app.blueprints.channel.routes.requires_auth') as mock_auth:
            def decorator(f):
                return f
            mock_auth.return_value = decorator
            yield mock_auth
    
    @pytest.fixture(autouse=True)
    def mock_limiter_storage(self):
        """Mock the limiter storage to avoid Redis dependency in tests."""
        with patch('app.extensions.limiter.storage') as mock_storage:
            mock_storage.get.return_value = None
            mock_storage.incr.return_value = 1
            yield mock_storage
    
    def test_channels_rate_limit_within_bounds(self, client, auth_headers, mock_auth_success):
        """Test that requests within rate limit are allowed for /channels."""
        with patch('app.blueprints.channel.routes.list_channels') as mock_list:
            mock_list.return_value = {"data": [], "meta": {"total": 0, "limit": 10, "offset": 0}}
            
            # Make multiple requests within the limit (30 per minute)
            for i in range(5):  # Well within the 30/minute limit
                response = client.get('/channels', headers=auth_headers)
                assert response.status_code == 200
    
    def test_export_rate_limit_within_bounds(self, client, auth_headers, mock_auth_success):
        """Test that requests within rate limit are allowed for /channels/export."""
        with patch('app.blueprints.channel.routes.export_channels') as mock_export:
            mock_export.return_value = MagicMock(status_code=200)
            
            # Make multiple requests within the limit (10 per minute for export)
            for i in range(3):  # Well within the 10/minute limit
                response = client.get('/channels/export', headers=auth_headers)
                assert response.status_code == 200
    
    def test_channel_by_id_rate_limit_within_bounds(self, client, auth_headers, mock_auth_success):
        """Test that requests within rate limit are allowed for /channels/<id>."""
        with patch('app.blueprints.channel.routes.get_channel_by_id') as mock_get:
            mock_get.return_value = {"data": {"id": 1, "title": "Test"}}
            
            # Make multiple requests within the limit (60 per minute)
            for i in range(10):  # Well within the 60/minute limit
                response = client.get('/channels/1', headers=auth_headers)
                assert response.status_code == 200
    
    @patch('app.extensions.limiter.storage')
    def test_channels_rate_limit_exceeded(self, mock_storage, client, auth_headers, mock_auth_success):
        """Test that rate limit is enforced for /channels endpoint."""
        # Mock storage to simulate rate limit exceeded
        mock_storage.get.return_value = 31  # Above the 30/minute limit
        mock_storage.incr.return_value = 31
        
        with patch('app.blueprints.channel.routes.list_channels') as mock_list:
            mock_list.return_value = {"data": [], "meta": {"total": 0, "limit": 10, "offset": 0}}
            
            response = client.get('/channels', headers=auth_headers)
            
        # Should be rate limited (429 Too Many Requests)
        assert response.status_code == 429
    
    @patch('app.extensions.limiter.storage')
    def test_export_rate_limit_exceeded(self, mock_storage, client, auth_headers, mock_auth_success):
        """Test that rate limit is enforced for /channels/export endpoint."""
        # Mock storage to simulate rate limit exceeded
        mock_storage.get.return_value = 11  # Above the 10/minute limit
        mock_storage.incr.return_value = 11
        
        with patch('app.blueprints.channel.routes.export_channels') as mock_export:
            mock_export.return_value = MagicMock(status_code=200)
            
            response = client.get('/channels/export', headers=auth_headers)
            
        # Should be rate limited (429 Too Many Requests)
        assert response.status_code == 429
    
    @patch('app.extensions.limiter.storage')
    def test_channel_by_id_rate_limit_exceeded(self, mock_storage, client, auth_headers, mock_auth_success):
        """Test that rate limit is enforced for /channels/<id> endpoint."""
        # Mock storage to simulate rate limit exceeded
        mock_storage.get.return_value = 61  # Above the 60/minute limit
        mock_storage.incr.return_value = 61
        
        with patch('app.blueprints.channel.routes.get_channel_by_id') as mock_get:
            mock_get.return_value = {"data": {"id": 1, "title": "Test"}}
            
            response = client.get('/channels/1', headers=auth_headers)
            
        # Should be rate limited (429 Too Many Requests)
        assert response.status_code == 429
    
    def test_rate_limit_headers_present(self, client, auth_headers, mock_auth_success):
        """Test that rate limit headers are present in responses."""
        with patch('app.blueprints.channel.routes.list_channels') as mock_list:
            mock_list.return_value = {"data": [], "meta": {"total": 0, "limit": 10, "offset": 0}}
            
            response = client.get('/channels', headers=auth_headers)
            
        # Check for rate limit headers (Flask-Limiter adds these)
        assert 'X-RateLimit-Limit' in response.headers or 'RateLimit-Limit' in response.headers


class TestChannelController:
    """Test the channel controller functions directly."""
    
    @patch('app.blueprints.channel.controller.get_channels_list')
    @patch('app.blueprints.channel.controller.get_pagination_params')
    @patch('app.blueprints.channel.controller.get_sorting_params')
    @patch('app.blueprints.channel.controller.get_search_query')
    def test_list_channels_controller_success(self, mock_search, mock_sorting, mock_pagination, mock_get_list):
        """Test successful channel listing via controller."""
        from app.blueprints.channel.controller import list_channels
        from flask import Flask
        
        # Setup mocks
        mock_search.return_value = None
        mock_sorting.return_value = ('id', 'asc')
        mock_pagination.return_value = (1, 10)
        mock_get_list.return_value = ([], {'total_items': 0})
        
        with Flask(__name__).test_request_context():
            result = list_channels()
        
        mock_get_list.assert_called_once_with(None, 'id', 'asc', 1, 10)
    
    @patch('app.blueprints.channel.controller.get_channel_detail')
    def test_get_channel_by_id_controller_success(self, mock_get_detail):
        """Test successful channel detail retrieval via controller."""
        from app.blueprints.channel.controller import get_channel_by_id
        
        mock_channel = MagicMock()
        mock_get_detail.return_value = mock_channel
        
        result = get_channel_by_id(1)
        
        mock_get_detail.assert_called_once_with(1)
    
    def test_get_channel_by_id_controller_invalid_id(self):
        """Test invalid channel ID handling."""
        from app.blueprints.channel.controller import get_channel_by_id
        
        with pytest.raises(ValidationError, match="Invalid channel ID"):
            get_channel_by_id(0)
    
    def test_get_channel_by_id_controller_string_id(self):
        """Test string channel ID handling."""
        from app.blueprints.channel.controller import get_channel_by_id
        
        with pytest.raises(ValidationError, match="Invalid channel ID"):
            get_channel_by_id("invalid")
    
    @patch('app.blueprints.channel.controller.get_channel_detail')
    def test_get_channel_by_id_controller_not_found(self, mock_get_detail):
        """Test channel not found handling."""
        from app.blueprints.channel.controller import get_channel_by_id
        
        mock_get_detail.side_effect = NotFoundError("Channel not found")
        
        with pytest.raises(NotFoundError):
            get_channel_by_id(999)
    
    @patch('app.blueprints.channel.controller.get_channel_detail')
    def test_get_channel_by_id_controller_database_error(self, mock_get_detail):
        """Test database error handling."""
        from app.blueprints.channel.controller import get_channel_by_id
        
        mock_get_detail.side_effect = Exception("Database error")
        
        with pytest.raises(DatabaseError, match="Failed to retrieve channel"):
            get_channel_by_id(1) 