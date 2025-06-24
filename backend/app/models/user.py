from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger
from datetime import datetime
# Update the import path below if "Base" is defined elsewhere, e.g., from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()
from sqlalchemy.ext.declarative import declarative_base
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
