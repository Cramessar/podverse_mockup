# backend/app/models/channel.py

from sqlalchemy import String, DateTime, Integer, Boolean, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.extensions import db
from app.models.base import Base
from app.models.account import StatsTrackAccountGuid
from app.models.stats import StatsAggregatedChannel, StatsTrackEventChannel


class Channel(Base):
    __tablename__ = "channel"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_text: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    slug: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    feed_id: Mapped[Optional[int]] = mapped_column(Integer, db.ForeignKey("feed.id"), nullable=True)
    podcast_index_id: Mapped[Optional[int]] = mapped_column(Integer)
    podcast_guid: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    sortable_title: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    medium_id: Mapped[Optional[int]] = mapped_column(Integer, db.ForeignKey("medium.id"), nullable=True)
    has_podcast_index_value: Mapped[bool] = mapped_column(Boolean, default=False)
    has_value_time_splits: Mapped[bool] = mapped_column(Boolean, default=False)

    feed = relationship("Feed", back_populates="channels")
    medium = relationship("Medium", back_populates="channels")
    categories = relationship(
        "ChannelCategory",
        back_populates="channel",
        cascade="all, delete-orphan"
    )
    items = relationship(
        "Item",
        back_populates="channel"
    )
    stats = relationship(
        "StatsAggregatedChannel",
        back_populates="channel",
        cascade="all, delete-orphan"
    )
    events = relationship(
        "StatsTrackEventChannel",
        back_populates="channel",
        cascade="all, delete-orphan"
    )


class ChannelCategory(Base):
    __tablename__ = "channel_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    channel_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("channel.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False)
    channel = relationship("Channel", back_populates="categories")
    category = relationship("Category", back_populates="channels")
