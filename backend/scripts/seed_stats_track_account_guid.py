# backend/scripts/seed_stats_track_account_guid.py

from seed_utils import get_db_session, unique_uuid
from app.models.account import StatsTrackAccountGuid, Account
from sqlalchemy.exc import SQLAlchemyError

BATCH_SIZE = 250  # PostgreSQL safe limit
LOG_FILE = "log_seed_guid.txt"

def seed_stats_track_account_guid():
    session = get_db_session()
    try:
        accounts = session.query(Account).all()
        if not accounts:
            msg = "⚠️  No accounts found. Please seed accounts first.\n"
            print(msg)
            log_to_file(msg)
            return

        new_guids = [
            StatsTrackAccountGuid(account_id=acct.id, account_guid=unique_uuid())
            for acct in accounts
            if not session.query(StatsTrackAccountGuid).filter_by(account_id=acct.id).first()
        ]

        if not new_guids:
            msg = "ℹ️  All accounts already have GUIDs assigned.\n"
            print(msg)
            log_to_file(msg)
            return

        log_to_file(f"📦 Seeding {len(new_guids)} new account GUIDs in batches of {BATCH_SIZE}...\n")
        print(f"📦 Seeding {len(new_guids)} new account GUIDs in batches of {BATCH_SIZE}...")

        for i in range(0, len(new_guids), BATCH_SIZE):
            batch = new_guids[i:i + BATCH_SIZE]
            session.add_all(batch)
            session.commit()
            msg = f"✅ Batch {i // BATCH_SIZE + 1}: Inserted {len(batch)} rows\n"
            print(msg.strip())
            log_to_file(msg)

        msg = f"🎉 Done! Total new GUIDs inserted: {len(new_guids)}\n"
        print(msg)
        log_to_file(msg)

        for g in new_guids[:3]:
            entry = f" - Account ID: {g.account_id}, GUID: {g.account_guid}\n"
            print(entry.strip())
            log_to_file(entry)

    except SQLAlchemyError as e:
        session.rollback()
        msg = f"❌ SQLAlchemy error during Account GUID seeding: {str(e)}\n"
        print(msg)
        log_to_file(msg)

    finally:
        session.close()

def log_to_file(message: str):
    """Appends a message to the debug log file."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message)

if __name__ == "__main__":
    seed_stats_track_account_guid()
