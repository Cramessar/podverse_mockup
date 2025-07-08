# backend/app/models/export_logs.py

from sqlalchemy import String, Integer, DateTime, Text, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.extensions import db
from app.models.base import Base

class ExportLog(Base):
    """Model for tracking export operations."""
    __tablename__ = 'export_logs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    admin_email: Mapped[str] = mapped_column(String(255), nullable=False)
    export_type: Mapped[str] = mapped_column(String(50), nullable=False)  # channels, feeds, items
    filters: Mapped[dict] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # pending, success, failed, skipped, expired
    file_path: Mapped[str] = mapped_column(Text, nullable=True)
    format: Mapped[str] = mapped_column(String(10), nullable=False)  # csv, json
    channels_count: Mapped[int] = mapped_column(Integer, nullable=True)
    feeds_count: Mapped[int] = mapped_column(Integer, nullable=True)
    items_count: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
