# backend/scripts/seed_stats_event_item.py

from seed_utils import get_db_session, fake
from app.models.account import StatsTrackAccountGuid
from app.models.item import Item, StatsTrackEventItem
from sqlalchemy.exc import IntegrityError
import random
from datetime import timedelta

def seed_stats_event_item(n=100):
    session = get_db_session()
    try:
        guids = session.query(StatsTrackAccountGuid).all()
        items = session.query(Item).all()

        if not guids or not items:
            print("⚠️  Missing account GUIDs or items. Please seed dependencies first.")
            return

        base_time = fake.date_time_between(start_date='-30d', end_date='-1d')
        events = []

        for _ in range(n):
            account_guid = random.choice(guids).account_guid
            item = random.choice(items)
            created_at = base_time + timedelta(minutes=random.randint(0, 43200))  # within 30 days

            event = StatsTrackEventItem(
                account_guid=account_guid,
                item_id=item.id,
                created_at=created_at
            )
            events.append(event)

        session.add_all(events)
        session.commit()

        print(f"✅ Seeded {len(events)} stats_track_event_item rows successfully")
        for e in events[:3]:
            print(f" - Item ID {e.item_id}, GUID: {e.account_guid}, Time: {e.created_at}")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting item events:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_stats_event_item()
