from flask import Blueprint

feed_bp = Blueprint('feeds', __name__)

from . import routes