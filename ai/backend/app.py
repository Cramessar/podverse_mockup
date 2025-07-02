# ai/backend/app.py

from flask import Flask, jsonify
import requests, os, time
from sync.blueprint_parser import extract_blueprint_routes
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Base, SyncedEntity
from sqlalchemy.exc import OperationalError
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine)

MAX_RETRIES = 10
RETRY_DELAY = 3
last_sync_time = None  # 🔄 Global variable to store last sync timestamp

for attempt in range(MAX_RETRIES):
    try:
        Base.metadata.create_all(engine)
        print("[DB INIT] SyncedEntity table created (or already exists).")
        break
    except OperationalError:
        print(f"[DB WAIT] Attempt {attempt+1}/{MAX_RETRIES} - Waiting {RETRY_DELAY}s...")
        time.sleep(RETRY_DELAY)
else:
    raise RuntimeError("🛑 Database not ready after multiple attempts.")

# 🔁 Sync Logic
def sync_all_data():
    global last_sync_time
    try:
        routes = extract_blueprint_routes()
        print(f"[ROUTES FOUND] {routes}")
        print(f"[SYNC START] Found {len(routes)} routes to sync.")
        session = SessionLocal()

        for name, path in routes.items():
            full_url = f"{BACKEND_URL}{path}"
            try:
                response = requests.get(full_url)
                response.raise_for_status()

                try:
                    json_data = response.json()
                except ValueError:
                    print(f"[ERROR] Failed to sync {name}: Invalid JSON")
                    print(f"[RESPONSE TEXT] {response.text[:300]}")
                    continue

                preview_data = json_data.get("data", json_data)

                if isinstance(preview_data, list):
                    for item in preview_data[:3]:
                        session.add(SyncedEntity(
                            entity_type=name.replace("_bp", ""),
                            source_url=full_url,
                            raw_data=item
                        ))
                else:
                    session.add(SyncedEntity(
                        entity_type=name.replace("_bp", ""),
                        source_url=full_url,
                        raw_data=preview_data
                    ))

                print(f"[SYNCED] {name}")
            except requests.exceptions.HTTPError as e:
                print(f"[ERROR] Failed to sync {name}: {e}")
            except Exception as e:
                print(f"[ERROR] Unexpected error syncing {name}: {e}")

        session.commit()
        session.close()
        last_sync_time = datetime.utcnow()
        print("[SYNC DONE] ✅ All routes synced.")
    except Exception as err:
        print(f"[FATAL] Sync error: {err}")

# 📊 Sync status helper
def get_sync_summary():
    session = SessionLocal()
    counts = (
        session.query(SyncedEntity.entity_type, func.count())
        .group_by(SyncedEntity.entity_type)
        .all()
    )
    total = session.query(func.count(SyncedEntity.id)).scalar()
    session.close()
    return {
        "last_sync_time": last_sync_time.isoformat() if last_sync_time else None,
        "total_synced": total,
        "entity_counts": {etype: count for etype, count in counts}
    }

# 🕒 Schedule it
scheduler = BackgroundScheduler()
scheduler.add_job(sync_all_data, "interval", minutes=10)
scheduler.start()

@app.route("/")
def health_check():
    return "AI container is alive. Background sync is running."

@app.route("/sync/all", methods=["GET"])
def manual_sync():
    sync_all_data()
    return jsonify({"status": "✅ Manual sync triggered"}), 200

@app.route("/sync/status", methods=["GET"])
def sync_status():
    return jsonify(get_sync_summary()), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
