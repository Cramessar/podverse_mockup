from seed_utils import get_db_session
from app.models.item import ItemFlagStatus
from sqlalchemy.exc import IntegrityError

item_flag_statuses = [
    "active",
    "pending-archive",
    "archived",
    "pending-delete"
]

def seed_item_flag_status():
    session = get_db_session()
    try:
        for status in item_flag_statuses:
            entry = ItemFlagStatus(status=status)
            session.add(entry)
        session.commit()
        print("✅ Item flag statuses seeded successfully")
    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting item flag statuses:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_item_flag_status()
