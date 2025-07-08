from datetime import datetime, timedelta
from seed_utils import get_db_session, fake
from app.models.feed import Feed, FeedLog
from sqlalchemy.exc import IntegrityError
import random

# Predefined realistic log scenarios
LOG_SCENARIOS = [
    {
        "status": 500,
        "errors": 1,
        "message": "Parsing failed: Malformed XML detected. Check for unclosed tags or invalid structure.",
    },
    {
        "status": 0,
        "errors": 1,
        "message": "Connection error: Unable to reach server. Verify feed URL or check firewall rules.",
    },
    {
        "status": 200,
        "errors": 0,
        "message": "Feed parsed successfully. All items updated with no issues.",
    },
    {
        "status": 404,
        "errors": 1,
        "message": "HTTP 404 Not Found: The requested RSS feed URL could not be located.",
    },
    {
        "status": 403,
        "errors": 1,
        "message": "Access Denied: HTTP 403 Forbidden. Server is blocking feed requests.",
    },
    {
        "status": 200,
        "errors": 0,
        "message": "Feed successfully parsed. 3 new items added, 1 item updated.",
    },
    {
        "status": 0,
        "errors": 1,
        "message": "Character Encoding Error: Unable to decode feed content using declared charset.",
    }
]

def seed_feed(n=10):
    session = get_db_session()
    try:
        for _ in range(n):
            url = fake.unique.url() + "/rss"
            feed = Feed(
                url=url,
                feed_flag_status_id=random.choices([1, 2, 3], weights=[0.6, 0.2, 0.2])[0],
                is_parsing=fake.boolean(chance_of_getting_true=10),
                parsing_priority=random.randint(0, 5),
                last_parsed_file_hash=fake.md5(),
                container_id=fake.bothify(text="##########"),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(feed)
            session.flush()  # So we can use feed.id before commit

            # Generate 1–3 log entries with useful diagnostic messages
            for _ in range(random.randint(1, 3)):
                scenario = random.choice(LOG_SCENARIOS)
                log = FeedLog(
                    feed_id=feed.id,
                    last_http_status=scenario["status"],
                    last_good_http_status_time=datetime.utcnow() - timedelta(days=random.randint(1, 5)),
                    last_finished_parse_time=datetime.utcnow() - timedelta(days=random.randint(0, 3)),
                    parse_errors=scenario["errors"],
                    message=scenario["message"]
                )
                session.add(log)

        session.commit()
        print(f"✅ Seeded {n} feeds with diverse statuses and logs successfully")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting feeds or logs:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_feed()
# This script seeds the database with realistic feed data and logs.