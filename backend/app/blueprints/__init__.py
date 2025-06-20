# app/blueprints/__init__.py

from flask import Blueprint
from .docs import docs_bp
from .channel import channel_bp
from .health import health_bp
from .feed import feed_bp
from .item import item_bp
from .category import category_bp
from .medium import medium_bp
from .stats import stats_bp


from app.db_test import db_test_bp
from app.sql_runner import sql_runner_bp


def register_blueprints(app):
    admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

    # Register all admin blueprints
    admin_bp.register_blueprint(docs_bp, url_prefix='/docs')
    admin_bp.register_blueprint(channel_bp, url_prefix='/channels')
    admin_bp.register_blueprint(feed_bp, url_prefix='/feeds')
    admin_bp.register_blueprint(item_bp, url_prefix='/items')
    admin_bp.register_blueprint(category_bp, url_prefix='/categories')
    admin_bp.register_blueprint(medium_bp, url_prefix='/mediums')
    admin_bp.register_blueprint(stats_bp, url_prefix='/stats')


    # Register main admin blueprint
    app.register_blueprint(admin_bp)
    
    # Register non-admin blueprints  
    app.register_blueprint(health_bp)
   
    # Register test/utility blueprints
    app.register_blueprint(db_test_bp)
    app.register_blueprint(sql_runner_bp)