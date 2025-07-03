# ai/backend/routes/__init__.py

from ai.backend.routes.sync_routes import sync_bp
from ai.backend.routes.admin_viewer import admin_viewer_bp  # 👈 Viewer for DB inspection

def register_routes(app):
    app.register_blueprint(sync_bp)
    app.register_blueprint(admin_viewer_bp)
