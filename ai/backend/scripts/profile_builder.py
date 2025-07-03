import logging
import requests
from sqlalchemy.exc import SQLAlchemyError
from ai.backend.db import SessionLocal
from ai.backend.models.synced_entity import SyncedEntity
from ai.backend.models.ai_profiles import AIChannelProfile

logger = logging.getLogger(__name__)


def fetch_channels(base_url):
    url = f"{base_url}/admin/channels"
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        if isinstance(json_data, list):
            return json_data
        elif isinstance(json_data, dict) and isinstance(json_data.get("data"), list):
            return json_data["data"]

        logger.error("[ERROR] Unexpected format from /admin/channels")
        return []

    except Exception as e:
        logger.error(f"[ERROR] Failed to fetch channels: {e}")
        return []


def run_combined_profile_builder(base_url=None):
    logger.info("🚀 Starting AI Profile Builder...")

    session = SessionLocal()
    inserted, skipped = 0, 0

    try:
        if base_url:
            logger.info("[🔄 SYNC MODE] Fetching live API data...")
            channels = fetch_channels(base_url)
            records = channels if isinstance(channels, list) else []
        else:
            logger.info("[📦 BLOB MODE] Loading from SyncedEntity table...")
            records = []
            entities = session.query(SyncedEntity).filter(SyncedEntity.entity_type == "channels").all()
            for entity in entities:
                raw = entity.raw_data
                if isinstance(raw, dict) and raw.get("id"):
                    records.append(raw)

        logger.info(f"[BUILD] Preparing {len(records)} records...")

        for ch in records:
            if not ch or not ch.get("id"):
                skipped += 1
                continue

            existing = session.query(AIChannelProfile).filter_by(source_id=ch["id"]).first()
            if existing:
                skipped += 1
                continue

            try:
                profile = AIChannelProfile(
                    source_id=ch["id"],
                    title=ch.get("title", "Untitled"),
                    slug=ch.get("slug", "no-slug"),
                    raw_data=ch
                )
                session.add(profile)
                inserted += 1
            except Exception as e:
                logger.warning(f"[SKIP] Failed to insert channel {ch.get('id')}: {e}")
                skipped += 1

        session.commit()
        logger.info(f"✅ AI Profiles Sync Complete — Inserted: {inserted}, Skipped: {skipped}")
    except SQLAlchemyError as db_err:
        logger.error(f"[DB ERROR] {db_err}")
    except Exception as e:
        logger.error(f"[FATAL] Could not run profile builder: {e}")
    finally:
        session.close()
