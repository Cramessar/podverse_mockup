from flask import Blueprint

export_logs_bp = Blueprint('export_logs', __name__)

from . import routes