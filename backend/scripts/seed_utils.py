from datetime import datetime, timedelta
import random
import uuid
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

# Initialize Faker
fake = Faker()

# Setup database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://podverse_admin:testest@database:5432/podverse_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Provides a new database session."""
    return SessionLocal()

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

def unique_uuid():
    """Returns a proper UUID object for database storage"""
    return uuid.uuid4()

def unique_uuid_str():
    """Returns a UUID as string for cases that need string representation"""
    return str(uuid.uuid4())

import time
import traceback

def run_seeder_with_retry(seeder_func, label="", retries=3, delay=3):
    attempt = 0
    while attempt < retries:
        try:
            print(f"🌱 Seeding {label} (Attempt {attempt + 1}/{retries})...")
            seeder_func()
            print(f"✅ {label} seeded successfully!\n")
            return
        except Exception as e:
            print(f"⚠️  Error seeding {label}: {e}")
            traceback.print_exc()
            attempt += 1
            time.sleep(delay)
    print(f"❌ Failed to seed {label} after {retries} attempts.\n")
