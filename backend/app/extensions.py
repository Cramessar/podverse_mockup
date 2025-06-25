# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from marshmallow import fields, validate, ValidationError
from flask_migrate import Migrate
import os

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

# Configure Flask-Limiter with Redis for production or in-memory for development/testing
def get_limiter_storage():
    """Return appropriate storage backend based on environment."""
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        # Production: use Redis
        return redis_url
    else:
        # Development/Testing: use in-memory storage
        return None

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per hour"],
    storage_uri=get_limiter_storage(),
    strategy="fixed-window"  # Can be "fixed-window", "moving-window", etc.
)
# add celery extension here