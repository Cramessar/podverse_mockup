# app/utils/auth.py

import json
from functools import wraps
from flask import request, _request_ctx_stack, abort
from jose import jwt
import requests
import os
from flask_limiter.util import get_remote_address

# 
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
ALGORITHMS = [os.getenv("ALGORITHMS", "RS256")]

# this class is used to raise an error when the auth is invalid
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    '''
    This function is used to get the token from the request headers
    if the token is not found, it will raise an error
    '''
    auth = request.headers.get("Authorization", None) # get the token from the request headers
    if not auth:
        raise AuthError({"code": "authorization_header_missing"}, 401)

    parts = auth.split() # split the token into parts

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header"}, 401)
    elif len(parts) != 2:
        raise AuthError({"code": "invalid_header"}, 401)

    return parts[1] # return the token

def requires_auth(f):
    '''
    This decorator is used to check if the user is authenticated
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header() 
        jsonurl = requests.get(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json") # get the jwks from the auth0 domain
        jwks = jsonurl.json() # parse the jwks
        unverified_header = jwt.get_unverified_header(token) # get the unverified header from the token

        # find the key in the jwks
        rsa_key = {}
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
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header"}, 400)

        _request_ctx_stack.top.current_user = payload
        return f(*args, **kwargs)

    return decorated



def get_limiter_key():
    """
    Return a unique key per user (Auth0 sub claim), or fallback to IP address.
    No signature verification for performance.
    """
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "")
    try:
        payload = jwt.get_unverified_claims(token)  # JOSE's fast decode without verify
        return payload.get("sub") or get_remote_address()
    except Exception:
        return get_remote_address()
