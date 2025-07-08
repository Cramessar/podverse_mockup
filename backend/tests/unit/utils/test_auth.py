import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, request
from jose import jwt
import json

from app.utils.auth import (
    AuthError, 
    get_token_auth_header, 
    requires_auth
)


class TestAuthError:
    """Test the AuthError exception class."""
    
    def test_auth_error_initialization(self):
        """Test AuthError is properly initialized with error and status code."""
        error = {"code": "test_error", "description": "Test error description"}
        status_code = 401
        
        auth_error = AuthError(error, status_code)
        
        assert auth_error.error == error
        assert auth_error.status_code == status_code


class TestGetTokenAuthHeader:
    """Test the get_token_auth_header function."""
    
    def test_missing_authorization_header(self, app):
        """Test that missing Authorization header raises AuthError."""
        with app.test_request_context() as ctx:
            # Don't mock request, just don't set the header
            with pytest.raises(AuthError) as exc_info:
                get_token_auth_header()
            
            assert exc_info.value.error["code"] == "authorization_header_missing"
            assert exc_info.value.status_code == 401
    
    def test_invalid_header_format_not_bearer(self, app):
        """Test that non-Bearer token raises AuthError."""
        with app.test_request_context() as ctx:
            ctx.request.headers = {"Authorization": "Basic sometoken"}
            
            with pytest.raises(AuthError) as exc_info:
                get_token_auth_header()
            
            assert exc_info.value.error["code"] == "invalid_header"
            assert exc_info.value.status_code == 401
    
    def test_invalid_header_format_wrong_parts(self, app):
        """Test that wrong number of parts in header raises AuthError."""
        with app.test_request_context() as ctx:
            ctx.request.headers = {"Authorization": "Bearer"}
            
            with pytest.raises(AuthError) as exc_info:
                get_token_auth_header()
            
            assert exc_info.value.error["code"] == "invalid_header"
            assert exc_info.value.status_code == 401
    
    def test_valid_authorization_header(self, app):
        """Test that valid Authorization header returns token."""
        token = "valid.jwt.token"
        with app.test_request_context() as ctx:
            ctx.request.headers = {"Authorization": f"Bearer {token}"}
            
            result = get_token_auth_header()
            
            assert result == token


class TestRequiresAuth:
    """Test the requires_auth decorator."""
    
    @patch('app.utils.auth.get_token_auth_header')
    @patch('app.utils.auth.requests.get')
    @patch('app.utils.auth.jwt.get_unverified_header')
    @patch('app.utils.auth.jwt.decode')
    @patch('app.utils.auth._request_ctx_stack')
    def test_successful_authentication(self, mock_ctx_stack, mock_jwt_decode, 
                                     mock_get_header, mock_requests, mock_get_token):
        """Test successful authentication flow."""
        # Setup mocks
        mock_get_token.return_value = "valid.jwt.token"
        mock_get_header.return_value = {"kid": "test-kid"}
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "keys": [{
                "kid": "test-kid",
                "kty": "RSA",
                "use": "sig",
                "n": "test-n",
                "e": "test-e"
            }]
        }
        mock_requests.return_value = mock_response
        
        mock_jwt_decode.return_value = {"sub": "user123", "aud": "test-audience"}
        
        # Create a test function
        @requires_auth
        def test_function():
            return "success"
        
        # Test the decorated function
        with patch.dict('os.environ', {
            'AUTH0_DOMAIN': 'test.auth0.com',
            'API_AUDIENCE': 'test-audience',
            'ALGORITHMS': 'RS256'
        }):
            result = test_function()
            
        assert result == "success"
        mock_jwt_decode.assert_called_once()
    
    @patch('app.utils.auth.get_token_auth_header')
    def test_missing_token_raises_error(self, mock_get_token):
        """Test that missing token raises AuthError."""
        mock_get_token.side_effect = AuthError({"code": "authorization_header_missing"}, 401)
        
        @requires_auth
        def test_function():
            return "success"
        
        with pytest.raises(AuthError) as exc_info:
            test_function()
        
        assert exc_info.value.error["code"] == "authorization_header_missing"
    
    @patch('app.utils.auth.get_token_auth_header')
    @patch('app.utils.auth.requests.get')
    @patch('app.utils.auth.jwt.get_unverified_header')
    def test_no_matching_key_raises_error(self, mock_get_header, mock_requests, mock_get_token):
        """Test that no matching key in JWKS raises AuthError."""
        mock_get_token.return_value = "valid.jwt.token"
        mock_get_header.return_value = {"kid": "unknown-kid"}
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "keys": [{
                "kid": "different-kid",
                "kty": "RSA",
                "use": "sig",
                "n": "test-n",
                "e": "test-e"
            }]
        }
        mock_requests.return_value = mock_response
        
        @requires_auth
        def test_function():
            return "success"
        
        with patch.dict('os.environ', {
            'AUTH0_DOMAIN': 'test.auth0.com',
            'API_AUDIENCE': 'test-audience'
        }):
            with pytest.raises(AuthError) as exc_info:
                test_function()
        
        assert exc_info.value.error["code"] == "no_key_found"
        assert exc_info.value.status_code == 401
    
    @patch('app.utils.auth.get_token_auth_header')
    @patch('app.utils.auth.requests.get')
    @patch('app.utils.auth.jwt.get_unverified_header')
    @patch('app.utils.auth.jwt.decode')
    def test_expired_token_raises_error(self, mock_jwt_decode, mock_get_header, 
                                      mock_requests, mock_get_token):
        """Test that expired token raises AuthError."""
        mock_get_token.return_value = "expired.jwt.token"
        mock_get_header.return_value = {"kid": "test-kid"}
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "keys": [{
                "kid": "test-kid",
                "kty": "RSA",
                "use": "sig",
                "n": "test-n",
                "e": "test-e"
            }]
        }
        mock_requests.return_value = mock_response
        
        mock_jwt_decode.side_effect = jwt.ExpiredSignatureError()
        
        @requires_auth
        def test_function():
            return "success"
        
        with patch.dict('os.environ', {
            'AUTH0_DOMAIN': 'test.auth0.com',
            'API_AUDIENCE': 'test-audience'
        }):
            with pytest.raises(AuthError) as exc_info:
                test_function()
        
        assert exc_info.value.error["code"] == "token_expired"
        assert exc_info.value.status_code == 401
    
    @patch('app.utils.auth.get_token_auth_header')
    @patch('app.utils.auth.requests.get')
    @patch('app.utils.auth.jwt.get_unverified_header')
    @patch('app.utils.auth.jwt.decode')
    def test_invalid_claims_raises_error(self, mock_jwt_decode, mock_get_header, 
                                       mock_requests, mock_get_token):
        """Test that invalid claims raise AuthError."""
        mock_get_token.return_value = "invalid.jwt.token"
        mock_get_header.return_value = {"kid": "test-kid"}
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "keys": [{
                "kid": "test-kid",
                "kty": "RSA",
                "use": "sig",
                "n": "test-n",
                "e": "test-e"
            }]
        }
        mock_requests.return_value = mock_response
        
        mock_jwt_decode.side_effect = jwt.JWTClaimsError()
        
        @requires_auth
        def test_function():
            return "success"
        
        with patch.dict('os.environ', {
            'AUTH0_DOMAIN': 'test.auth0.com',
            'API_AUDIENCE': 'test-audience'
        }):
            with pytest.raises(AuthError) as exc_info:
                test_function()
        
        assert exc_info.value.error["code"] == "invalid_claims"
        assert exc_info.value.status_code == 401 