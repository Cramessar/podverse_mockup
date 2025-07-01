# backend/scripts/seed_stats_aggregated_item.py

from seed_utils import get_db_session
from app.models.item import Item, StatsAggregatedItem
from sqlalchemy.exc import IntegrityError
import random

def seed_stats_aggregated_item():
    session = get_db_session()
    try:
        items = session.query(Item).all()
        if not items:
            print("⚠️  No items found. Please seed items first.")
            return

        # Check for already-seeded items to avoid duplication
        existing = session.query(StatsAggregatedItem.item_id).all()
        existing_ids = {row[0] for row in existing}
        new_items = [item for item in items if item.id not in existing_ids]

        if not new_items:
            print("✅ All items already have stats. Skipping.")
            return

        aggregates = []
        for item in new_items:
            base = random.randint(20, 120)
            week_base = base * 7
            month_base = week_base * 4

            agg = StatsAggregatedItem(
                item_id=item.id,
                day_current_count=base,
                day_1_count=int(base * 0.95),
                day_2_count=int(base * 0.85),
                day_3_count=int(base * 0.75),
                day_4_count=int(base * 0.65),
                day_5_count=int(base * 0.55),
                day_6_count=int(base * 0.45),
                day_7_count=int(base * 0.35),
                day_8_count=int(base * 0.25),
                week_current_count=week_base,
                week_1_count=int(week_base * 0.9),
                week_2_count=int(week_base * 0.8),
                week_3_count=int(week_base * 0.7),
                week_4_count=int(week_base * 0.6),
                month_current_count=month_base,
                month_1_count=int(month_base * 0.85),
                all_time_count=month_base + random.randint(500, 2500)
            )
            aggregates.append(agg)

        session.add_all(aggregates)
        session.commit()

        print(f"✅ Seeded {len(aggregates)} new stats_aggregated_item entries.")
        for a in aggregates[:3]:  # Preview first 3
            print(f" - Item ID {a.item_id} | Daily: {a.day_current_count}, Weekly: {a.week_current_count}, All-time: {a.all_time_count}")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting aggregated item stats:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_stats_aggregated_item()
