# app/utils/audit_decorators.py

from functools import wraps
from flask import request
from app.utils.security_logger import log_admin_action
from app.utils.request_logger import get_logger

def audit_admin_access(action: str, resource: str):
    """
    Decorator to audit admin access to specific resources to add on the routes.
    This is used to log the admin actions to the database.
    Usage: @audit_admin_access(action="REPARSE_FEED", resource="feed")

    Args:
        action: Type of admin action (create, read, update, delete)
        resource: Name of the resource being accessed
    """ 
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            logger = get_logger("admin_audit")

            user = getattr(request, "user", None)  # Replace with real Auth0 user context if needed
            user_id = getattr(user, "sub", "unknown") if user else "unknown"

            resource_id = kwargs.get("id") or kwargs.get(f"{resource}_id") or "unknown"
            log_admin_action(
                logger=logger,
                user_id=user_id,
                action=action,
                resource=resource,
                resource_id=resource_id,
                details=f"{request.method} {request.path}"
            )
            return fn(*args, **kwargs)
        return wrapper
    return decorator
