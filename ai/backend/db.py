# ai/backend/db.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Central declarative base shared by all models
Base = declarative_base()

# Create engine from environment or use fallback
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ai_user:password@localhost:5432/ai_profiles")
engine = create_engine(DATABASE_URL)

# Session factory to be used throughout the app
SessionLocal = sessionmaker(bind=engine)
