# app/blueprints/__init__.py

from app.blueprints.docs.routes import docs_bp
from .podcast.routes import podcast_bp

def register_blueprints(app):
    app.register_blueprint(docs_bp)  # Register docs blueprint for OpenAPI/Swagger
    app.register_blueprint(podcast_bp, url_prefix="/admin/podcast")