# backend/app/utils/limiter_utils.py

from flask import request
from jose import jwt
from flask_limiter.util import get_remote_address
import os
from typing import Optional, Union

def get_limiter_key() -> str:
    """
    Return a unique key per user (Auth0 sub claim), or fallback to IP address.
    No signature verification for performance.
    
    Returns:
        str: Either the Auth0 subject ID or the client's IP address
    """
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "")
    try:
        payload = jwt.get_unverified_claims(token)  # JOSE's fast decode without verify
        return str(payload.get("sub") or get_remote_address())
    except Exception:
        return str(get_remote_address())

# Configure Flask-Limiter with Redis for production or in-memory for development/testing
def get_limiter_storage() -> Optional[str]:
    """
    Return appropriate storage backend based on environment.
    
    Returns:
        Optional[str]: Redis URL for production, None for development/testing
    """
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        # Production: use Redis
        return redis_url
    else:
        # Development/Testing: use in-memory storage
        return None