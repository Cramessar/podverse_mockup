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
    def test_list_channels_controller(self, mock_search, mock_sort, mock_pagination, mock_get_list):
        """Test the list_channels controller function."""
        from app.blueprints.channel.controller import list_channels
        
        # Setup mocks
        mock_pagination.return_value = (1, 10)  # page, limit
        mock_sort.return_value = ('id', 'asc')  # sort_by, sort_order
        mock_search.return_value = 'test search'
        
        mock_channels = [{'id': 1, 'title': 'Test Channel'}]
        mock_meta = {'total_items': 1}
        mock_get_list.return_value = (mock_channels, mock_meta)
        
        with patch('app.blueprints.channel.controller.request') as mock_request:
            result = list_channels()
            
        # Verify the result structure
        assert 'data' in result.json
        assert 'meta' in result.json
        assert result.json['meta']['total'] == 1
        assert result.json['meta']['limit'] == 10
        assert result.json['meta']['offset'] == 0
    
    @patch('app.blueprints.channel.controller.get_channel_detail')
    def test_get_channel_by_id_controller_success(self, mock_get_detail):
        """Test the get_channel_by_id controller function with valid ID."""
        from app.blueprints.channel.controller import get_channel_by_id
        
        mock_channel = {'id': 1, 'title': 'Test Channel'}
        mock_get_detail.return_value = mock_channel
        
        result = get_channel_by_id(1)
        
        # Verify the result
        assert 'id' in result.json
        mock_get_detail.assert_called_once_with(1)
    
    def test_get_channel_by_id_controller_invalid_id(self):
        """Test the get_channel_by_id controller function with invalid ID."""
        from app.blueprints.channel.controller import get_channel_by_id
        
        with pytest.raises(ValidationError) as exc_info:
            get_channel_by_id(-1)
        
        assert "Invalid channel ID" in str(exc_info.value)
    
    def test_get_channel_by_id_controller_string_id(self):
        """Test the get_channel_by_id controller function with string ID."""
        from app.blueprints.channel.controller import get_channel_by_id
        
        with pytest.raises(ValidationError) as exc_info:
            get_channel_by_id("invalid")
        
        assert "Invalid channel ID" in str(exc_info.value)
    
    @patch('app.blueprints.channel.controller.get_channel_detail')
    def test_get_channel_by_id_controller_not_found(self, mock_get_detail):
        """Test the get_channel_by_id controller when channel is not found."""
        from app.blueprints.channel.controller import get_channel_by_id
        
        mock_get_detail.side_effect = NotFoundError("Channel not found")
        
        with pytest.raises(NotFoundError):
            get_channel_by_id(999)
    
    @patch('app.blueprints.channel.controller.get_channel_detail')
    def test_get_channel_by_id_controller_database_error(self, mock_get_detail):
        """Test the get_channel_by_id controller when database error occurs."""
        from app.blueprints.channel.controller import get_channel_by_id
        
        mock_get_detail.side_effect = Exception("Database connection failed")
        
        with pytest.raises(DatabaseError) as exc_info:
            get_channel_by_id(1)
        
        assert "Failed to retrieve channel" in str(exc_info.value) 