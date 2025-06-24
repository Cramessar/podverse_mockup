from flask import Blueprint

# Admin blueprints
from app.blueprints.docs import docs_bp
from app.blueprints.channel import channel_bp
from app.blueprints.health import health_bp
from app.blueprints.feed import feed_bp
from app.blueprints.item import item_bp
from app.blueprints.category import category_bp
from app.blueprints.medium import medium_bp
from app.blueprints.stats import stats_bp
from app.blueprints.site import site_bp

# Utility/test blueprints
from app.db_test import db_test_bp
from app.sql_runner import sql_runner_bp


def register_blueprints(app):
    # Top-level /admin blueprint
    admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

    # All routes below will become /admin/<something>
    admin_bp.register_blueprint(docs_bp, url_prefix="/docs")
    admin_bp.register_blueprint(channel_bp, url_prefix="/channels")
    admin_bp.register_blueprint(feed_bp, url_prefix="/feeds")
    admin_bp.register_blueprint(item_bp, url_prefix="/items")
    admin_bp.register_blueprint(category_bp, url_prefix="/categories")
    admin_bp.register_blueprint(medium_bp, url_prefix="/mediums")
    admin_bp.register_blueprint(stats_bp, url_prefix="/stats")
    admin_bp.register_blueprint(site_bp, url_prefix="/site")

    # Register the grouped admin routes
    app.register_blueprint(admin_bp)

    # Global routes (not under /admin)
    app.register_blueprint(health_bp)
    app.register_blueprint(db_test_bp)
    app.register_blueprint(sql_runner_bp)
