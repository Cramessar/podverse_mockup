# ai/backend/models/synced_entity.py

from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from ai.backend.db import Base

class SyncedEntity(Base):
    __tablename__ = "synced_entities"

    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String(100), nullable=False)  # 👈 Add this
    entity_type = Column(String(100), nullable=False)
    url = Column(String(255), nullable=False)
    raw_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
