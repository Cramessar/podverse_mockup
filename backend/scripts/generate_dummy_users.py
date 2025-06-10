from datetime import datetime, timedelta
import random
import uuid

from faker import Faker
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    BigInteger,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

fake = Faker()
Base = declarative_base()

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

def main():
    # Connect to your actual database here:
    engine = create_engine("postgresql://podverse_admin:testest@database:5432/podverse_db")

    # Drop and recreate tables (WARNING: drops all data)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    users = []
    for _ in range(200):
        email = fake.unique.email()
        username = fake.user_name()
        role = "admin" if random.random() < 0.05 else "user"  # 5% admins
        created_at = random_past_date()
        last_login = random_past_date()
        is_active = random.random() > 0.1  # 90% active
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
    print(f"Inserted {len(users)} dummy users into the database.")

if __name__ == "__main__":
    main()
