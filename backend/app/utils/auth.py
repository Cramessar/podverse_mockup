# app/utils/auth.py

from functools import wraps
from typing import Dict, Any, Callable, TypeVar, cast
from flask import request, _request_ctx_stack, current_app
from jose import jwt
import requests
from app.utils.error_exceptions import AuthError
from app.utils.security_logger import log_auth_event

def get_auth0_config() -> Dict[str, Any]:
    """Get Auth0 configuration from current app config.

    Returns:
        Dict[str, Any]: Dictionary containing AUTH0_DOMAIN, API_AUDIENCE, and ALGORITHMS
    """
    return {
        "AUTH0_DOMAIN": current_app.config["AUTH0_DOMAIN"],
        "API_AUDIENCE": current_app.config["API_AUDIENCE"],
        "ALGORITHMS": [current_app.config.get("ALGORITHMS", "RS256")]
    }

def get_token_auth_header() -> str:
    """Extract and validate bearer token from request headers.
    
    Returns:
        str: The extracted JWT token
        
    Raises:
        AuthError: If token is missing or invalid
    """
    auth = request.headers.get("Authorization", None) # get the token from the request headers
    if not auth:
        raise AuthError({"code": "authorization_header_missing"}, 401)

    parts = auth.split() # split the token into parts for bearer token

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header"}, 401)
    elif len(parts) != 2:
        raise AuthError({"code": "invalid_header"}, 401)

    return parts[1] # return the token

# Define a generic type for the decorated function
F = TypeVar('F', bound=Callable[..., Any])

def requires_auth(f: F) -> F:
    """Decorator to verify JWT token and authenticate requests.
    
    Args:
        f (Callable): The function type to decorate
        
    Returns:
        Callable: The decorated function with authentication
        
    Raises:
        AuthError: If token validation fails
    """
    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        token = get_token_auth_header() 
        jsonurl = requests.get(f"https://{current_app.config['AUTH0_DOMAIN']}/.well-known/jwks.json") # get the jwks from the auth0 domain
        jwks = jsonurl.json() # parse the jwks
        unverified_header = jwt.get_unverified_header(token) # get the unverified header from the token

        # find the key in the jwks
        rsa_key: Dict[str, str] = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]: # if the kid is the same as the kid in the token then set the rsa key
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

        if not rsa_key:
            raise AuthError({"code": "no_key_found"}, 401)

        try: # decode the token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=current_app.config["ALGORITHMS"],
                audience=current_app.config["API_AUDIENCE"],
                issuer=f"https://{current_app.config['AUTH0_DOMAIN']}/"
            )
            log_auth_event(logger, "TOKEN_VALID", payload["sub"], "Token validated successfully")
        except jwt.ExpiredSignatureError:
            log_auth_event(logger, "TOKEN_EXPIRED", "unknown", "Token expired")
            raise AuthError({"code": "token_expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header"}, 400)

        _request_ctx_stack.top.current_user = payload
        return f(*args, **kwargs)

    return cast(F, decorated)