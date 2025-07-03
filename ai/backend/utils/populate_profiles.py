# ai/backend/utils/populate_profiles.py

from ai.backend.models.synced_entity import SyncedEntity
from ai.backend.models.ai_profiles import AIChannelProfile
from ai.backend.db import SessionLocal
from sqlalchemy.exc import SQLAlchemyError


def populate_ai_profiles():  # ✅ Updated function name
    session = SessionLocal()
    try:
        # 🧠 Step 1: Filter for synced channel data
        channel_entities = session.query(SyncedEntity).filter(SyncedEntity.entity_type == "channel").all()
        print(f"[STRUCTURE] Found {len(channel_entities)} channel entities to process.")

        inserted, skipped = 0, 0

        # 🛠 Step 2: Loop and transform into AIChannelProfile entries
        for entity in channel_entities:
            data = entity.raw_data
            if not data or not data.get("id"):
                skipped += 1
                continue

            # Check if profile already exists
            if session.query(AIChannelProfile).filter_by(source_id=data["id"]).first():
                skipped += 1
                continue

            try:
                profile = AIChannelProfile(
                    source_id=data["id"],
                    title=data.get("title"),
                    slug=data.get("slug"),
                    raw_data=data,
                )
                session.add(profile)
                inserted += 1
            except Exception as e:
                print(f"[❌] Failed to process channel ID {data.get('id')}: {e}")

        session.commit()
        print(f"✅ Channel profiles populated. Inserted: {inserted}, Skipped: {skipped}")
    except SQLAlchemyError as e:
        print(f"[DB ERROR] {e}")
    except Exception as e:
        print(f"[FATAL] Unhandled error during profile population: {e}")
    finally:
        session.close()
