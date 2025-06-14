# app/blueprints/__init__.py

from app.blueprints.docs.routes import docs_bp
from app.blueprints.channel.routes import channel_bp

from app.db_test import db_test_bp
from app.sql_runner import sql_runner_bp

def register_blueprints(app):
    app.register_blueprint(docs_bp)  # OpenAPI/Swagger docs
    app.register_blueprint(channel_bp, url_prefix="/admin/channel")

    # Register your new blueprints
    app.register_blueprint(db_test_bp)
    app.register_blueprint(sql_runner_bp)
