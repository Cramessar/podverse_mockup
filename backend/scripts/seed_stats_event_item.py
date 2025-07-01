from seed_utils import get_db_session, fake
from app.models.account import StatsTrackAccountGuid
from app.models.item import Item
from app.models.item import StatsTrackEventItem
from sqlalchemy.exc import IntegrityError
import random

def seed_stats_event_item(n=100):
    session = get_db_session()
    try:
        guids = session.query(StatsTrackAccountGuid).all()
        items = session.query(Item).all()

        if not guids or not items:
            print("⚠️  Missing account GUIDs or items. Please seed dependencies first.")
            return

        events = []
        for _ in range(n):
            event = StatsTrackEventItem(
                account_guid=random.choice(guids).account_guid,
                item_id=random.choice(items).id,
                created_at=fake.date_time_between(start_date='-30d', end_date='now')
            )
            events.append(event)

        session.add_all(events)
        session.commit()
        print(f"✅ Seeded {n} stats_track_event_item rows successfully")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting item events:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_stats_event_item()