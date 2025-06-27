from seed_utils import get_db_session, unique_uuid
from app.models.account import StatsTrackAccountGuid, Account
from sqlalchemy.exc import IntegrityError

def seed_stats_track_account_guid():
    session = get_db_session()
    try:
        accounts = session.query(Account).all()
        if not accounts:
            print("⚠️  No accounts found. Please seed accounts first.")
            return

        guids = []
        for account in accounts:
            guid = StatsTrackAccountGuid(
                account_id=account.id,
                account_guid=unique_uuid()
            )
            guids.append(guid)

        session.add_all(guids)
        session.commit()
        print(f"✅ Seeded {len(guids)} stats_track_account_guid rows successfully")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting account GUIDs:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_stats_track_account_guid()
