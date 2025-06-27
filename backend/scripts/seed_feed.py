from datetime import datetime
from seed_utils import get_db_session, fake
from app.models.feed import Feed
from sqlalchemy.exc import IntegrityError
import random

def seed_feed(n=10):
    session = get_db_session()
    feeds = []
    try:
        for _ in range(n):
            url = fake.unique.url() + "/rss"
            feed = Feed(
                url=url,
                feed_flag_status_id=1,  # Assumes "active" is seeded and has ID=1
                is_parsing=fake.boolean(chance_of_getting_true=10),
                parsing_priority=random.randint(0, 5),
                last_parsed_file_hash=fake.md5(),
                container_id=fake.bothify(text="##########"),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            feeds.append(feed)
        session.add_all(feeds)
        session.commit()
        print(f"✅ Seeded {n} feeds successfully")
    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting feeds:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_feed()
