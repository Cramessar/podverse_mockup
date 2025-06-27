from seed_utils import get_db_session
from app.models.item import Item, StatsAggregatedItem
from sqlalchemy.exc import IntegrityError
import random

def seed_stats_aggregated_item(n=20):
    session = get_db_session()
    try:
        items = session.query(Item).all()
        if not items:
            print("⚠️  No items found. Please seed items first.")
            return

        aggregates = []
        for _ in range(n):
            item = random.choice(items)
            agg = StatsAggregatedItem(
                item_id=item.id,
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
        print(f"✅ Seeded {len(aggregates)} stats_aggregated_item rows successfully")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting aggregated item stats:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_stats_aggregated_item()