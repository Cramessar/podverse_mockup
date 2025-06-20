# app/blueprints/__init__.py

from flask import Blueprint
from .docs import docs_bp
from .channel import channel_bp
from .health import health_bp
from .feed import feed_bp
from .item import item_bp

from app.db_test import db_test_bp
from app.sql_runner import sql_runner_bp


def register_blueprints(app):
    admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

    admin_bp.register_blueprint(docs_bp, url_prefix='/docs')
    admin_bp.register_blueprint(channel_bp, url_prefix='/channels')
    admin_bp.register_blueprint(feed_bp, url_prefix='/feeds')
    admin_bp.register_blueprint(item_bp, url_prefix='/items')

    app.register_blueprint(admin_bp)
    app.register_blueprint(health_bp)
   
   # Register your new blueprints
    app.register_blueprint(db_test_bp)
    app.register_blueprint(sql_runner_bp)