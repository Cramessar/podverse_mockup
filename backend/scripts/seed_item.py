from seed_utils import get_db_session, fake
from app.models.item import Item
from app.models.channel import Channel
from app.models.item import ItemFlagStatus
from sqlalchemy.exc import IntegrityError
import random
from datetime import datetime

def seed_item(n=20):
    session = get_db_session()
    try:
        channels = session.query(Channel).all()
        statuses = session.query(ItemFlagStatus).all()

        if not channels:
            print("⚠️  No channels found. Please seed channels first.")
            return
        if not statuses:
            print("⚠️  No item flag statuses found. Please seed item_flag_status first.")
            return

        items = []
        for _ in range(n):
            channel = random.choice(channels)
            status = random.choice(statuses)
            item = Item(
                id_text=fake.unique.slug(),
                slug=fake.slug(),
                channel_id=channel.id,
                guid=fake.uri(),
                guid_enclosure_url=fake.url(),
                pub_date=fake.date_time_between(start_date='-1y', end_date='now'),
                title=fake.sentence(nb_words=6),
                item_flag_status_id=status.id
            )
            items.append(item)

        session.add_all(items)
        session.commit()
        print(f"✅ Seeded {len(items)} items successfully")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting items:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_item()
