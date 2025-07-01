from seed_utils import get_db_session, fake
from app.models.account import StatsTrackAccountGuid
from app.models.channel import Channel
from app.models.channel import StatsTrackEventChannel
from sqlalchemy.exc import IntegrityError
import random

def seed_stats_event_channel(n=100):
    session = get_db_session()
    try:
        guids = session.query(StatsTrackAccountGuid).all()
        channels = session.query(Channel).all()

        if not guids or not channels:
            print("⚠️  Missing account GUIDs or channels. Please seed dependencies first.")
            return

        events = []
        for _ in range(n):
            event = StatsTrackEventChannel(
                account_guid=random.choice(guids).account_guid,
                channel_id=random.choice(channels).id,
                created_at=fake.date_time_between(start_date='-30d', end_date='now')
            )
            events.append(event)

        session.add_all(events)
        session.commit()
        print(f"✅ Seeded {n} stats_track_event_channel rows successfully")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting channel events:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_stats_event_channel()