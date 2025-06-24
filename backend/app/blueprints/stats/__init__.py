from flask import Blueprint

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')

from . import routes 