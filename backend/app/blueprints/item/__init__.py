from flask import Blueprint

item_bp = Blueprint('item', __name__)

from . import routes 