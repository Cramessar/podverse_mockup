# backend/scripts/seed_sharable_status.py

from seed_utils import get_db_session
from app.models.account import SharableStatus

def seed_sharable_status():
    session = get_db_session()
    try:
        default_statuses = [
            (1, "public"),
            (2, "unlisted"),
            (3, "private")
        ]

        for status_id, status in default_statuses:
            exists = session.query(SharableStatus).filter_by(id=status_id).first()
            if not exists:
                entry = SharableStatus(
                    id=status_id,
                    status=status
                )
                session.add(entry)
                print(f"✅ Inserted sharable_status: {status}")
            else:
                print(f"ℹ️ Sharable status '{status}' already exists")

        session.commit()
    except Exception as e:
        session.rollback()
        print("⚠️ Error seeding sharable_status:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_sharable_status()
