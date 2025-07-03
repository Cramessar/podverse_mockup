# ai/backend/app.py

from flask import Flask, jsonify
import os, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from apscheduler.schedulers.background import BackgroundScheduler

from ai.backend.routes import register_routes
from ai.backend.models.synced_entity import Base
from ai.backend.utils.sync_utils import sync_all_data, get_sync_summary  # ✅ Updated import

app = Flask(__name__)
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine)

MAX_RETRIES = 10
RETRY_DELAY = 3

# 📦 Create DB tables
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

# 🕒 Schedule background sync
scheduler = BackgroundScheduler()
scheduler.add_job(lambda: sync_all_data(engine, BACKEND_URL), "interval", minutes=10)
scheduler.start()

# 🔗 Register all routes
register_routes(app)

@app.route("/")
def health_check():
    return "AI container is alive. Background sync is running."

@app.route("/sync/status", methods=["GET"])
def sync_status():
    return jsonify(get_sync_summary(engine)), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
