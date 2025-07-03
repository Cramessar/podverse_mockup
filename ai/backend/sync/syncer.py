# ai/backend/sync/syncer.py

import requests
from ai.backend.sync.blueprint_parser import extract_blueprint_routes
from ai.backend.models.synced_entity import SyncedEntity
from ai.backend.db import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

BASE_BACKEND_URL = "http://backend:8000"  # Docker alias for podverse backend


def sync_all_routes():
    routes = extract_blueprint_routes()
    print(f"[SYNC START] Found {len(routes)} routes to sync.")

    session = SessionLocal()

    for name, path in routes.items():
        full_url = f"{BASE_BACKEND_URL}{path}"

        try:
            response = requests.get(full_url)
            response.raise_for_status()

            # Ensure we're working with JSON content
            content_type = response.headers.get("Content-Type", "")
            if "application/json" not in content_type:
                print(f"[SKIP] {name} returned non-JSON content type: {content_type}")
                print(f"[RESPONSE TEXT] \n{response.text}")
                continue

            data = response.json()
            entity_type = path.rstrip("/").split("/")[-1]  # e.g., /admin/channels → "channels"

            synced = SyncedEntity(
                route_name=name,
                entity_type=entity_type,
                url=full_url,
                raw_data=data,
            )

            session.add(synced)
            print(f"[SYNCED] {name}")

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to sync {name}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[RESPONSE TEXT] \n{e.response.text}")
        except ValueError as json_err:
            print(f"[ERROR] Failed to parse JSON for {name}: {json_err}")
            print(f"[RESPONSE TEXT] \n{response.text}")
        except SQLAlchemyError as db_err:
            print(f"[DB ERROR] Could not save {name}: {db_err}")

    try:
        session.commit()
    except SQLAlchemyError as commit_err:
        print(f"[DB ERROR] Commit failed: {commit_err}")
    finally:
        session.close()

    print("[SYNC DONE] ✅ All routes synced.")
    return routes
