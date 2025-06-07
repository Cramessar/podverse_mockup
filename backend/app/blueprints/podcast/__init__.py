# app/blueprints/podcast/__init__.py

from flask import Blueprint

podcast_bp = Blueprint("podcast", __name__) 

from . import routes
