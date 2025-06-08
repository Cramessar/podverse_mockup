from flask import Blueprint

bp = Blueprint('item', __name__, url_prefix='/item')

from . import routes 