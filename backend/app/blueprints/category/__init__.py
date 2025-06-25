# app/blueprints/category/__init__.py

from flask import Blueprint

category_bp = Blueprint('category', __name__, url_prefix='/categories')

from . import routes 