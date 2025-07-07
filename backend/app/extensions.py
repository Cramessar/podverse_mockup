# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_migrate import Migrate
from marshmallow import fields, validate
from app.utils.limiter_utils import get_limiter_key, get_limiter_storage

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

limiter = Limiter(
    key_func=get_limiter_key,
    default_limits=["1000 per hour"],
    storage_uri=get_limiter_storage(),
    strategy="fixed-window"
)