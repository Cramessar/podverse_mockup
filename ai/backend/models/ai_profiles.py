# ai/backend/models/ai_profiles.py

from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean
from sqlalchemy.sql import func
from ai.backend.db import Base 

class AIChannelProfile(Base):
    __tablename__ = 'ai_channel_profiles'

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, nullable=False, unique=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    publisher = Column(String, nullable=True)
    feed_url = Column(String, nullable=True)
    medium_id = Column(Integer, nullable=True)
    has_value_time_splits = Column(Boolean, nullable=True)
    has_podcast_index_value = Column(Boolean, nullable=True)
    raw_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<AIChannelProfile(id={self.id}, source_id={self.source_id}, title='{self.title}')>"
