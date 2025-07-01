# backend/scripts/seed_stats_track_account_guid.py

from seed_utils import get_db_session, unique_uuid
from app.models.account import StatsTrackAccountGuid, Account
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

def seed_stats_track_account_guid():
    session = get_db_session()
    try:
        accounts = session.query(Account).all()
        if not accounts:
            print("⚠️  No accounts found. Please seed accounts first.")
            return

        guids = []

        for account in accounts:
            # Check if a GUID already exists for this account
            existing_guid = session.query(StatsTrackAccountGuid).filter_by(account_id=account.id).first()
            if existing_guid:
                continue  # Skip to avoid duplicates

            guid = StatsTrackAccountGuid(
                account_id=account.id,
                account_guid=unique_uuid()
            )
            guids.append(guid)

        if not guids:
            print("ℹ️  All accounts already have GUIDs assigned.")
            return

        session.add_all(guids)
        session.commit()
        print(f"✅ Seeded {len(guids)} stats_track_account_guid rows successfully")

        for g in guids[:3]:
            print(f" - Account ID: {g.account_id}, GUID: {g.account_guid}")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting account GUIDs:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_stats_track_account_guid()
