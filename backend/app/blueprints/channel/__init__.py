# app/blueprints/channel/__init__.py

from flask import Blueprint

channel_bp = Blueprint("channels", __name__)
from . import routes
