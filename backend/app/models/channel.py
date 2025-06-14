from sqlalchemy import String, Text, DateTime, Integer, UUID
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.extensions import db
from app.models.base import Base  

class Channel(Base):
    __tablename__ = "channel"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_text: Mapped[Optional[str]] = mapped_column(String(15), unique=True)
    slug: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    feed_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True)
    podcast_index_id: Mapped[Optional[int]] = mapped_column(Integer)
    podcast_guid: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    sortable_title: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    medium_id: Mapped[Optional[int]] = mapped_column(Integer)
