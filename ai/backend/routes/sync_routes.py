# ai/backend/routes/sync_routes.py

import os
from flask import Blueprint, jsonify
from ai.backend.sync.syncer import sync_all_routes
from ai.backend.scripts.profile_builder import run_combined_profile_builder

sync_bp = Blueprint("sync", __name__, url_prefix="/sync")
BASE_BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

@sync_bp.route("/all", methods=["GET"])
def sync_everything():
    try:
        print("[SYNC] Syncing routes...")
        routes = sync_all_routes()

        print("[SYNC] Enriching AI profiles from live backend...")
        run_combined_profile_builder(base_url=BASE_BACKEND_URL)

        return jsonify({
            "status": "success",
            "synced_routes": list(routes.keys())
        }), 200

    except Exception as e:
        print(f"[❌ SYNC ERROR] {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@sync_bp.route("/status", methods=["GET"])
def sync_status():
    return jsonify({"message": "Sync status endpoint is active."}), 200
