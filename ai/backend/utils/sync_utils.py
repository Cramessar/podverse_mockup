import requests
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from ai.backend.models.synced_entity import SyncedEntity
from ai.backend.sync.blueprint_parser import extract_blueprint_routes
from ai.backend.scripts.profile_builder import run_combined_profile_builder

SessionLocal = sessionmaker()
last_sync_time = None 


def sync_all_data(database_engine, backend_url):
    global last_sync_time
    SessionLocal.configure(bind=database_engine)

    try:
        routes = extract_blueprint_routes()
        print(f"[ROUTES FOUND] {routes}")
        print(f"[SYNC START] Found {len(routes)} routes to sync.")
        session = SessionLocal()

        for route_name, path in routes.items():
            full_url = f"{backend_url}{path}"
            try:
                response = requests.get(full_url)
                response.raise_for_status()

                try:
                    json_data = response.json()
                except ValueError:
                    print(f"[ERROR] Failed to sync {route_name}: Invalid JSON")
                    print(f"[RESPONSE TEXT] {response.text[:300]}")
                    continue

                entity_type = path.split("/")[-1] 
                preview_data = json_data.get("data", json_data)

                if isinstance(preview_data, list):
                    for item in preview_data[:3]:
                        session.add(SyncedEntity(
                            route_name=route_name,
                            entity_type=entity_type,
                            source_url=full_url,
                            raw_data=item
                        ))
                else:
                    session.add(SyncedEntity(
                        route_name=route_name,
                        entity_type=entity_type,
                        source_url=full_url,
                        raw_data=preview_data
                    ))

                print(f"[SYNCED] {route_name}")
            except requests.exceptions.HTTPError as e:
                print(f"[ERROR] Failed to sync {route_name}: {e}")
            except Exception as e:
                print(f"[ERROR] Unexpected error syncing {route_name}: {e}")

        session.commit()
        session.close()
        last_sync_time = datetime.utcnow()
        print("[SYNC DONE] ✅ All routes synced.")

        # debugging, remove later
        print("[PROFILE ENRICHMENT] Building AI profiles from synced blobs...")
        run_combined_profile_builder()  # This uses blob mode automatically
        print("[PROFILE ENRICHMENT DONE] ✅ Profiles synced.")

    except Exception as err:
        print(f"[FATAL] Sync error: {err}")


def get_sync_summary(database_engine):
    SessionLocal.configure(bind=database_engine)
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
