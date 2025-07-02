# ai/backend/models.py

from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SyncedEntity(Base):
    __tablename__ = "synced_entities"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String, nullable=False)  # e.g., "channel", "feed"
    source_url = Column(String, nullable=False)
    raw_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
