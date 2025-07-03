# ai/backend/app.py

from flask import Flask, jsonify
import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from apscheduler.schedulers.background import BackgroundScheduler

from ai.backend.routes import register_routes
from ai.backend.models.synced_entity import Base
from ai.backend.utils.sync_utils import sync_all_data, get_sync_summary
from ai.backend.utils.auto_migrate import auto_migrate
from ai.backend.utils.ensure_schema import add_missing_tables, add_missing_columns  # 🧠 New import

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
        print(f"[DB WAIT] Attempt {attempt + 1}/{MAX_RETRIES} - Waiting {RETRY_DELAY}s...")
        time.sleep(RETRY_DELAY)
else:
    raise RuntimeError("🛑 Database not ready after multiple attempts.")

# 🧠 Patch schema if any tables or fields are missing
add_missing_tables()
add_missing_columns()

# 🕒 Schedule background sync
scheduler = BackgroundScheduler()
scheduler.add_job(lambda: sync_all_data(engine, BACKEND_URL), "interval", minutes=10)
scheduler.start()

auto_migrate()

# Register all routes with safe debug wrapper
print("[DEBUG] Starting Flask app...")
try:
    register_routes(app)
    print("[✅] Routes registered successfully.")
except Exception as e:
    print(f"[❌] Route registration failed: {e}")

# sanity check, dont judge me
@app.route("/")
def health_check():
    return "AI container is alive. Background sync is running."

@app.route("/sync/status", methods=["GET"])
def sync_status():
    return jsonify(get_sync_summary(engine)), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
