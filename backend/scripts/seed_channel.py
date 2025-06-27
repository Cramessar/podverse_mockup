from seed_utils import get_db_session, fake, unique_uuid
from app.models.channel import Channel
from app.models.feed import Feed
from app.models.medium import Medium
from sqlalchemy.exc import IntegrityError
import random

def seed_channel(n=10):
    session = get_db_session()
    try:
        feeds = session.query(Feed).all()
        mediums = session.query(Medium).all()
        if not feeds:
            print("⚠️  No feeds found. Please seed feeds first.")
            return

        channels = []
        for _ in range(n):
            feed = random.choice(feeds)
            medium_id = random.choice(mediums).id if mediums else None
            channel = Channel(
                id_text=fake.unique.user_name(),
                slug=fake.slug(),
                feed_id=feed.id,
                podcast_index_id=random.randint(1000, 9999),
                podcast_guid=unique_uuid(),
                title=fake.sentence(nb_words=3),
                sortable_title=fake.word().lower(),
                medium_id=medium_id,
                has_podcast_index_value=fake.boolean(chance_of_getting_true=30),
                has_value_time_splits=fake.boolean(chance_of_getting_true=20)
            )
            channels.append(channel)

        session.add_all(channels)
        session.commit()
        print(f"✅ Seeded {len(channels)} channels successfully")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting channels:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_channel()