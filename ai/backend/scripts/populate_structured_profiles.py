# ai/backend/scripts/populate_structured_profiles.py

from ai.backend.models.synced_entity import SyncedEntity
from ai.backend.models.ai_profiles import AIChannelProfile
from ai.backend.db import SessionLocal
from sqlalchemy.exc import IntegrityError


def populate_ai_profiles():
    session = SessionLocal()
    try:
        # Filter only channel entities
        channel_entities = session.query(SyncedEntity).filter(SyncedEntity.entity_type == "channel").all()
        print(f"[PROFILE BUILD] Found {len(channel_entities)} synced channels to process.")

        for entity in channel_entities:
            data = entity.raw_data
            if not data:
                continue

            existing = session.query(AIChannelProfile).filter_by(source_id=data.get("id")).first()
            if existing:
                continue  # Skip duplicates

            try:
                profile = AIChannelProfile(
                    source_id=data.get("id"),
                    title=data.get("title"),
                    slug=data.get("slug"),
                    raw_data=data
                )
                session.add(profile)
            except Exception as e:
                print(f"[❌] Failed to add profile for channel ID {data.get('id')}: {e}")

        session.commit()
        print("✅ Channel profiles populated.")
    except Exception as e:
        print(f"[FATAL] Could not populate AI profiles: {e}")
    finally:
        session.close()
