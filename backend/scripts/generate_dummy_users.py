from datetime import datetime, timedelta
import random
import uuid
import os

from faker import Faker
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    BigInteger,
    ForeignKey,
    create_engine,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# testing use of db connection to the podverse database.
db_url = os.getenv("DATABASE_URL", "postgresql://podverse_admin:testest@database:5432/podverse_db")
print(f"Connecting to database at: {db_url}")
engine = create_engine(db_url)

fake = Faker()
Base = declarative_base()

# ----------------- Your Existing User Model -----------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(50), nullable=False)
    role = Column(String(20), default="user")  # user/admin
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    total_listen_time_seconds = Column(BigInteger, default=0)
    referral_token = Column(String(36), unique=True, nullable=False)  # UUID string
    device_info = Column(String(255))
    location = Column(String(100))

# ----------------- Podverse Models -----------------
class Feed(Base):
    __tablename__ = "feed"
    id = Column(Integer, primary_key=True)
    url = Column(String(255), unique=True, nullable=False)
    feed_flag_status_id = Column(Integer, nullable=False)  # Assume seeded with ID=1

    channels = relationship("Channel", back_populates="feed")

class Channel(Base):
    __tablename__ = "channel"
    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey("feed.id"), nullable=False)
    id_text = Column(String(255), nullable=False)
    podcast_index_id = Column(Integer, nullable=False)

    feed = relationship("Feed", back_populates="channels")
    items = relationship("Item", back_populates="channel")

class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey("channel.id"), nullable=False)
    id_text = Column(String(255), nullable=False)

    channel = relationship("Channel", back_populates="items")

class StatsTrackAccountGuid(Base):
    __tablename__ = "stats_track_account_guid"
    id = Column(Integer, primary_key=True)
    account_guid = Column(String(255), unique=True, nullable=False)

class StatsTrackEventItem(Base):
    __tablename__ = "stats_track_event_item"
    id = Column(Integer, primary_key=True)
    stats_track_account_guid_id = Column(Integer, ForeignKey("stats_track_account_guid.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    event_timestamp = Column(DateTime, nullable=False)

class StatsAggregatedItem(Base):
    __tablename__ = "stats_aggregated_item"
    item_id = Column(Integer, ForeignKey("item.id"), primary_key=True)
    day = Column(DateTime, primary_key=True)
    listen_count = Column(Integer)

# ----------------- Helper Functions -----------------

def random_past_date(within_days=365):
    return datetime.utcnow() - timedelta(
        days=random.randint(0, within_days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )

def random_device_info():
    devices = [
        "iPhone 14, iOS 16.4",
        "Samsung Galaxy S22, Android 13",
        "Chrome on Windows 10",
        "Firefox on macOS",
        "Safari on iPadOS",
        "Edge on Windows 11",
        "Android Tablet",
        "Linux Desktop",
    ]
    return random.choice(devices)

def random_location():
    countries = [
        "USA",
        "Canada",
        "UK",
        "Australia",
        "Germany",
        "France",
        "India",
        "Brazil",
    ]
    return random.choice(countries)

# ----------------- Podverse Data Generators -----------------

def generate_users(session, n=200):
    users = []
    for _ in range(n):
        email = fake.unique.email()
        username = fake.user_name()
        role = "admin" if random.random() < 0.05 else "user"
        created_at = random_past_date()
        last_login = random_past_date()
        is_active = random.random() > 0.1
        total_listen_time_seconds = random.randint(0, 10_000_000)
        referral_token = str(uuid.uuid4())
        device_info = random_device_info()
        location = random_location()

        user = User(
            email=email,
            username=username,
            role=role,
            created_at=created_at,
            last_login=last_login,
            is_active=is_active,
            total_listen_time_seconds=total_listen_time_seconds,
            referral_token=referral_token,
            device_info=device_info,
            location=location,
        )
        users.append(user)
    session.add_all(users)
    session.commit()
    print(f"Inserted {n} dummy users.")

def generate_feeds(session, n=5):
    feeds = []
    for _ in range(n):
        feed = Feed(
            url=fake.unique.url() + "/rss",
            feed_flag_status_id=1,  # Assuming seeded
        )
        feeds.append(feed)
    session.add_all(feeds)
    session.commit()
    print(f"Inserted {n} feeds.")
    return feeds

def generate_channels(session, feeds, n=10):
    channels = []
    for _ in range(n):
        feed = random.choice(feeds)
        channel = Channel(
            feed_id=feed.id,
            id_text=fake.unique.user_name(),
            podcast_index_id=fake.random_int(1000, 9999),
        )
        channels.append(channel)
    session.add_all(channels)
    session.commit()
    print(f"Inserted {n} channels.")
    return channels

def generate_items(session, channels, n=20):
    items = []
    for _ in range(n):
        channel = random.choice(channels)
        item = Item(
            channel_id=channel.id,
            id_text=fake.unique.slug(),
        )
        items.append(item)
    session.add_all(items)
    session.commit()
    print(f"Inserted {n} items.")
    return items

def generate_account_guids(session, n=10):
    guids = []
    for _ in range(n):
        guid = StatsTrackAccountGuid(account_guid=str(uuid.uuid4()))
        guids.append(guid)
    session.add_all(guids)
    session.commit()
    print(f"Inserted {n} stats_track_account_guid rows.")
    return guids

def generate_event_items(session, guids, items, n=50):
    events = []
    for _ in range(n):
        event = StatsTrackEventItem(
            stats_track_account_guid_id=random.choice(guids).id,
            item_id=random.choice(items).id,
            event_timestamp=fake.date_time_between(start_date='-30d', end_date='now'),
        )
        events.append(event)
    session.add_all(events)
    session.commit()
    print(f"Inserted {n} stats_track_event_item rows.")

def generate_aggregated_items(session, items, n=10):
    aggregated = []
    for _ in range(n):
        item = random.choice(items)
        day = fake.date_time_between(start_date='-10d', end_date='now').date()
        aggregated.append(
            StatsAggregatedItem(
                item_id=item.id,
                day=day,
                listen_count=random.randint(1, 500),
            )
        )
    session.add_all(aggregated)
    session.commit()
    print(f"Inserted {n} stats_aggregated_item rows.")

# ----------------- Main runner -----------------

def main():
    global engine  # use the engine created from env var

    with engine.connect() as conn:
        print("Dropping schema public and recreating it safely...")
        conn.execution_options(isolation_level="AUTOCOMMIT").execute(text("""
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'public') THEN
                    EXECUTE 'DROP SCHEMA public CASCADE';
                END IF;
                EXECUTE 'CREATE SCHEMA public';
            END
            $$;
        """))

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    generate_users(session)
    feeds = generate_feeds(session)
    channels = generate_channels(session, feeds)
    items = generate_items(session, channels)
    guids = generate_account_guids(session)
    generate_event_items(session, guids, items)
    generate_aggregated_items(session, items)

    session.close()
    print("Finished seeding Podverse mock data!")


if __name__ == "__main__":
    main()
