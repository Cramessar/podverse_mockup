## ai/backend/routes/sync_routes.py

from flask import Blueprint, jsonify
from ai.backend.sync.syncer import sync_all_routes
from ai.backend.utils.populate_profiles import populate_ai_profiles
from ai.backend.utils.sync_utils import get_sync_summary
from ai.backend.db import engine  # 👈 Central import from db.py

sync_bp = Blueprint("sync", __name__, url_prefix="/sync")


@sync_bp.route("/all", methods=["GET"])
def sync_everything():
    routes = sync_all_routes()
    print("[SYNC] Routes synced. Now populating AI profiles...")
    populate_ai_profiles()
    return jsonify({
        "status": "success",
        "synced_routes": list(routes.keys())
    })


@sync_bp.route("/status", methods=["GET"])
def sync_status():
    print("[📊] Returning sync summary...")
    return jsonify(get_sync_summary(engine)), 200
