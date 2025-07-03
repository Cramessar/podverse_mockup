# ai/backend/models/ai_profiles.py

from sqlalchemy import Column, Integer, String, JSON
from ai.backend.db import Base  # Shared declarative base

class AIChannelProfile(Base):
    __tablename__ = 'ai_channel_profiles'

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, nullable=False, unique=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    raw_data = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<AIChannelProfile(id={self.id}, source_id={self.source_id}, title='{self.title}')>"
