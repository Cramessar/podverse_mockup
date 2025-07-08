# backend/scripts/seed_stats_aggregated_channel.py

from seed_utils import get_db_session
from app.models.stats import StatsAggregatedChannel
from app.models.channel import Channel
from sqlalchemy.exc import IntegrityError
import random

def seed_stats_aggregated_channel():
    session = get_db_session()
    try:
        channels = session.query(Channel).all()
        if not channels:
            print("⚠️  No channels found. Please seed channels first.")
            return

        aggregates = []
        existing = session.query(StatsAggregatedChannel.channel_id).all()
        existing_ids = {row[0] for row in existing}

        new_channels = [c for c in channels if c.id not in existing_ids]
        if not new_channels:
            print("✅ All channels already have stats. Skipping.")
            return

        for channel in new_channels:
            base = random.randint(50, 150)
            week_base = base * 7
            month_base = week_base * 4

            agg = StatsAggregatedChannel(
                channel_id=channel.id,
                day_current_count=base,
                day_1_count=int(base * 0.9),
                day_2_count=int(base * 0.8),
                day_3_count=int(base * 0.7),
                day_4_count=int(base * 0.6),
                day_5_count=int(base * 0.5),
                day_6_count=int(base * 0.4),
                day_7_count=int(base * 0.3),
                day_8_count=int(base * 0.2),
                week_current_count=week_base,
                week_1_count=int(week_base * 0.9),
                week_2_count=int(week_base * 0.8),
                week_3_count=int(week_base * 0.7),
                week_4_count=int(week_base * 0.6),
                month_current_count=month_base,
                month_1_count=int(month_base * 0.8),
                all_time_count=month_base + random.randint(1000, 3000)
            )
            aggregates.append(agg)

        session.add_all(aggregates)
        session.commit()

        print(f"✅ Seeded {len(aggregates)} new stats_aggregated_channel entries.")
        for a in aggregates[:3]:  # Preview first 3
            print(f" - Channel ID {a.channel_id} | Daily: {a.day_current_count}, Weekly: {a.week_current_count}, All-time: {a.all_time_count}")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting aggregated channel stats:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_stats_aggregated_channel()
