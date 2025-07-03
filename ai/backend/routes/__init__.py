## ai/backend/routes/__init__.py
from ai.backend.routes.sync_routes import sync_bp
from ai.backend.routes.admin_viewer import admin_viewer_bp
from ai.backend.routes.ollama_routes import ollama_bp
from ai.backend.routes.report_routes import report_bp

def register_routes(app):
    app.register_blueprint(sync_bp)
    app.register_blueprint(admin_viewer_bp)
    app.register_blueprint(ollama_bp)  # 🧠 NEW
    app.register_blueprint(report_bp)