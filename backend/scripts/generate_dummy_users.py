from datetime import datetime, timedelta
import random
import uuid
import os
import time
import traceback

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

# Database connection from docker-compose or environment variable
db_url = os.getenv("DATABASE_URL", "postgresql://podverse_admin:testest@database:5432/podverse_db")
print(f"[DB] Connecting to: {db_url}")
engine = create_engine(db_url)

fake = Faker()
Base = declarative_base()

# ----------------- Models -----------------

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


class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(50), nullable=False)
    created_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

    stats_account_guid = relationship("StatsTrackAccountGuid", back_populates="account", uselist=False)


class StatsTrackAccountGuid(Base):
    __tablename__ = "stats_track_account_guid"
    id = Column(Integer, primary_key=True)
    account_guid = Column(String(255), unique=True, nullable=False)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)

    account = relationship("Account", back_populates="stats_account_guid")


class StatsTrackEventChannel(Base):
    __tablename__ = "stats_track_event_channel"
    id = Column(Integer, primary_key=True)
    stats_track_account_guid_id = Column(Integer, ForeignKey("stats_track_account_guid.id"), nullable=False)
    channel_id = Column(Integer, ForeignKey("channel.id"), nullable=False)
    event_timestamp = Column(DateTime, nullable=False)


class StatsAggregatedChannel(Base):
    __tablename__ = "stats_aggregated_channel"
    channel_id = Column(Integer, ForeignKey("channel.id"), primary_key=True)
    day = Column(DateTime, primary_key=True)
    listen_count = Column(Integer)


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


# ----------------- Data Generators Logic -----------------

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
            feed_flag_status_id=1, # Assuming feed_flag_status_id=1 is a valid seeded ID
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


def generate_accounts(session, n=100):
    accounts = []
    for _ in range(n):
        email = fake.unique.email()
        username = fake.user_name()
        created_at = random_past_date()
        is_active = random.random() > 0.1
        account = Account(email=email, username=username, created_at=created_at, is_active=is_active)
        accounts.append(account)
    session.add_all(accounts)
    session.commit()
    print(f"Inserted {n} accounts.")
    return accounts


def generate_stats_account_guids(session, accounts):
    guids = []
    for account in accounts:
        guid = StatsTrackAccountGuid(account_guid=str(uuid.uuid4()), account_id=account.id)
        guids.append(guid)
    session.add_all(guids)
    session.commit()
    print(f"Inserted {len(guids)} stats_track_account_guid rows.")
    return guids


def generate_stats_track_event_channels(session, guids, channels, n=100):
    events = []
    for _ in range(n):
        event = StatsTrackEventChannel(
            stats_track_account_guid_id=random.choice(guids).id,
            channel_id=random.choice(channels).id,
            event_timestamp=fake.date_time_between(start_date='-30d', end_date='now')
        )
        events.append(event)
    session.add_all(events)
    session.commit()
    print(f"Inserted {n} stats_track_event_channel rows.")


def generate_stats_aggregated_channels(session, channels, n=20):
    aggregated = []
    for _ in range(n):
        channel = random.choice(channels)
        day = fake.date_time_between(start_date='-10d', end_date='now').date()
        aggregated.append(
            StatsAggregatedChannel(
                channel_id=channel.id,
                day=day,
                listen_count=random.randint(1, 500),
            )
        )
    session.add_all(aggregated)
    session.commit()
    print(f"Inserted {n} stats_aggregated_channel rows.")


# ----------------- Main runner -----------------

def main():
    global engine

    try:
        with engine.connect() as conn:
            print("[DB] Dropping and recreating public schema...")
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
    except Exception as e:
        print("[ERROR] Could not reset schema:")
        traceback.print_exc()
        raise

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        generate_users(session)
        feeds = generate_feeds(session)
        channels = generate_channels(session, feeds)
        items = generate_items(session, channels)
        user_guids = generate_account_guids(session)
        generate_event_items(session, user_guids, items)
        generate_aggregated_items(session, items)
        accounts = generate_accounts(session)
        account_guids = generate_stats_account_guids(session, accounts)
        generate_stats_track_event_channels(session, account_guids, channels)
        generate_stats_aggregated_channels(session, channels)
        print("✅ Finished seeding Podverse mock data!")
    except Exception as e:
        print("[ERROR] Seeding process failed:")
        traceback.print_exc()
    finally:
        session.close()

# ----------------- Retry Wrapper -----------------

def safe_main():
    max_retries = 5
    for i in range(max_retries):
        try:
            print(f"[SEED] Attempt {i + 1} of {max_retries}")
            main()
            return
        except Exception as e:
            print(f"[ERROR] Seeding attempt {i+1} failed: {e}")
            traceback.print_exc()
            time.sleep(5)

    print("❌ Dummy data generation failed after 5 attempts.")

if __name__ == "__main__":
    safe_main()