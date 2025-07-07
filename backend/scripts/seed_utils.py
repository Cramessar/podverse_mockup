# backend/scripts/seed_utils.py
from datetime import datetime, timedelta
import random
from uuid import uuid4
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import uuid
<<<<<<< HEAD

=======
from sqlalchemy.orm import Session
from app.extensions import db
from app.utils.logger import get_logger
>>>>>>> cb05fd0 (feat: implement Celery reparse and scheduled data export functionality)

# Initialize Faker
fake = Faker()

# Setup database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://podverse_admin:testest@database:5432/podverse_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = get_logger(__name__)

def get_db_session() -> Session:
    """Get a database session."""
    return db.session

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

def unique_uuid() -> str:
    """Generate a unique UUID."""
    return str(uuid.uuid4())

def unique_uuid_str():
    """Returns a UUID as string for cases that need string representation"""
    return str(uuid.uuid4())

import time
import traceback

def run_seeder_with_retry(seeder_func, max_retries=3):
    """Run a seeder function with retries."""
    for attempt in range(max_retries):
        try:
            seeder_func()
            return True
        except Exception as e:
            logger.warning(f"Error seeding: {str(e)}")
            if attempt < max_retries - 1:
                continue
            else:
                logger.error(f"Failed to seed after {max_retries} attempts.")
                return False
