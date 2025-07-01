from seed_utils import get_db_session
from app.models.account import SharableStatus
from datetime import datetime


def seed_sharable_status():
    session = get_db_session()
    try:
        default_statuses = [
            (1, "public"),
            (2, "unlisted"),
            (3, "private")
        ]

        for status_id, label in default_statuses:
            exists = session.query(SharableStatus).filter_by(id=status_id).first()
            if not exists:
                entry = SharableStatus(
                    id=status_id,
                    label=label,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(entry)
                print(f"Inserted sharable_status: {label}")
            else:
                print(f"Sharable status '{label}' already exists")

        session.commit()
    except Exception as e:
        session.rollback()
        print("⚠️  Error seeding sharable_status:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_sharable_status()