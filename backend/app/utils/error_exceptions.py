# app/utils/error_exceptions.py

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