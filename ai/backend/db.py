# ai/backend/db.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# declarative base shared by all models
Base = declarative_base()


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ai_user:password@localhost:5432/ai_profiles")
engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(bind=engine)
