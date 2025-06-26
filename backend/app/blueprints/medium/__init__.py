from flask import Blueprint

medium_bp = Blueprint('medium', __name__, url_prefix='/mediums')

from . import routes 