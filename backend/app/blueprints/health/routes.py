# app/blueprints/health/routes.py

from . import health_bp
from flask import jsonify

@health_bp.route("/health")
def index():
    return jsonify({"status": "API running"})

@health_bp.route("/admin")
def admin_root():
    print("health/routes.py loaded")
    return jsonify({"message": "Admin API is up and running"})
