from seed_utils import get_db_session
from app.models.channel import Channel, StatsAggregatedChannel
from sqlalchemy.exc import IntegrityError
import random

def seed_stats_aggregated_channel(n=20):
    session = get_db_session()
    try:
        channels = session.query(Channel).all()
        if not channels:
            print("⚠️  No channels found. Please seed channels first.")
            return

        aggregates = []
        for _ in range(n):
            channel = random.choice(channels)
            agg = StatsAggregatedChannel(
                channel_id=channel.id,
                day_current_count=random.randint(10, 100),
                day_1_count=random.randint(10, 100),
                day_2_count=random.randint(10, 100),
                day_3_count=random.randint(10, 100),
                day_4_count=random.randint(10, 100),
                day_5_count=random.randint(10, 100),
                day_6_count=random.randint(10, 100),
                day_7_count=random.randint(10, 100),
                day_8_count=random.randint(10, 100),
                week_current_count=random.randint(100, 500),
                week_1_count=random.randint(100, 500),
                week_2_count=random.randint(100, 500),
                week_3_count=random.randint(100, 500),
                week_4_count=random.randint(100, 500),
                month_current_count=random.randint(500, 1000),
                month_1_count=random.randint(500, 1000),
                all_time_count=random.randint(1000, 5000)
            )
            aggregates.append(agg)

        session.add_all(aggregates)
        session.commit()
        print(f"✅ Seeded {len(aggregates)} stats_aggregated_channel rows successfully")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting aggregated channel stats:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_stats_aggregated_channel()