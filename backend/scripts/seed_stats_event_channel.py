# backend/scripts/seed_stats_event_channel.py

from seed_utils import get_db_session, fake
from app.models.account import StatsTrackAccountGuid
from app.models.channel import Channel
from app.models.stats import StatsTrackEventChannel
from sqlalchemy.exc import IntegrityError
import random
from datetime import timedelta

def seed_stats_event_channel(n=100):
    session = get_db_session()
    try:
        guids = session.query(StatsTrackAccountGuid).all()
        channels = session.query(Channel).all()

        if not guids or not channels:
            print("⚠️  Missing account GUIDs or channels. Please seed dependencies first.")
            return

        events = []
        base_date = fake.date_time_between(start_date='-30d', end_date='-1d')

        for _ in range(n):
            # Simulate burst patterns and repeated listening
            account_guid = random.choice(guids).account_guid
            channel = random.choice(channels)
            created_at = base_date + timedelta(minutes=random.randint(0, 43200))  # within 30 days

            event = StatsTrackEventChannel(
                account_guid=account_guid,
                channel_id=channel.id,
                created_at=created_at
            )
            events.append(event)

        session.add_all(events)
        session.commit()

        print(f"✅ Seeded {len(events)} stats_track_event_channel events successfully")
        for e in events[:3]:
            print(f" - Channel ID {e.channel_id}, GUID: {e.account_guid}, Time: {e.created_at}")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting channel events:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_stats_event_channel()
