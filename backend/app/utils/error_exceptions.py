# app/utils/error_exceptions.py

from typing import Dict, Optional

class APIException(Exception):
    """Base class for API exceptions."""
    status_code = 500
    message = "Internal Server Error"

    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def __str__(self):
        return f"{self.message} (Status Code: {self.status_code})"
    
class AuthError(Exception):
    """Exception raised for authentication errors."""
    
    def __init__(self, error: Dict[str, str], status_code: int) -> None:
        self.error = error
        self.status_code = status_code

class ValidationError(APIException):
    """Exception raised for validation errors."""
    status_code = 400
    message = "Validation Error"
    
class NotFoundError(APIException):
    """Exception raised when a resource is not found."""
    status_code = 404
    message = "Resource Not Found"
    
class DatabaseError(APIException):
    """Exception raised for database-related errors."""
    status_code = 500
    message = "Database Error"

class DuplicateFeedError(APIException):
    """Exception raised when attempting to create a duplicate feed."""
    status_code = 409
    message = "Feed already exists"

class ParseError(Exception):
    """Raised when feed parsing fails."""

    def __init__(self, message, feed_id=None, url=None, bozo_exception=None):
        super().__init__(message)
        self.feed_id = feed_id
        self.url = url
        self.bozo_exception = bozo_exception

    def __str__(self):
        parts = [f"ParseError: {self.args[0]}"]
        if self.feed_id:
            parts.append(f"(Feed ID: {self.feed_id})")
        if self.url:
            parts.append(f"(URL: {self.url})")
        if self.bozo_exception:
            parts.append(f"(Bozo: {repr(self.bozo_exception)})")
        return " ".join(parts)

class RedisLockError(APIException):
    """Exception raised for Redis locking errors."""
    status_code = 500
    message = "Redis Lock Error"

    def __init__(self, message: str, lock_name: Optional[str] = None) -> None:
        super().__init__(message=message, status_code=self.status_code)
        self.lock_name = lock_name

    def __str__(self) -> str:
        base_msg = super().__str__()
        if self.lock_name:
            return f"{base_msg} (Lock: {self.lock_name})"
        return base_msg
