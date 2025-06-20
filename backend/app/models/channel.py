from sqlalchemy import String, DateTime, Integer, Boolean, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.extensions import db
from app.models.base import Base  

class Channel(Base):
    __tablename__ = "channel"

id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
id_text: Mapped[Optional[str]] = mapped_column(String(15), unique=True)
slug: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
feed_id: Mapped[Optional[int]] = mapped_column(Integer, db.ForeignKey("feed.id"), nullable=True)
podcast_index_id: Mapped[Optional[int]] = mapped_column(Integer)
podcast_guid: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), unique=True)
title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
sortable_title: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
medium_id: Mapped[Optional[int]] = mapped_column(Integer)
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
    "StatsAggreatedChannel", 
    back_populates="channel", 
    cascade="all, delete-orphan"
)
events = relationship(
    "StatsTrackEventChannel", 
    back_populates="channel", 
    cascade="all, delete-orphan"
)

class StatsAggreatedChannel(Base):
    __tablename__ = "stats_aggregated_channel"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("channel.id"), nullable=False)
    day_current_count: Mapped[int] = mapped_column(Integer, default=0)
    day_1_count: Mapped[int] = mapped_column(Integer, default=0)
    day_2_count: Mapped[int] = mapped_column(Integer, default=0)
    day_3_count: Mapped[int] = mapped_column(Integer, default=0)
    day_4_count: Mapped[int] = mapped_column(Integer, default=0)
    day_5_count: Mapped[int] = mapped_column(Integer, default=0)
    day_6_count: Mapped[int] = mapped_column(Integer, default=0)
    day_7_count: Mapped[int] = mapped_column(Integer, default=0)
    day_8_count: Mapped[int] = mapped_column(Integer, default=0)
    week_current_count: Mapped[int] = mapped_column(Integer, default=0)
    week_1_count: Mapped[int] = mapped_column(Integer, default=0)
    week_2_count: Mapped[int] = mapped_column(Integer, default=0)
    week_3_count: Mapped[int] = mapped_column(Integer, default=0)
    week_4_count: Mapped[int] = mapped_column(Integer, default=0)
    month_current_count: Mapped[int] = mapped_column(Integer, default=0)
    month_1_count: Mapped[int] = mapped_column(Integer, default=0)
    all_time_count: Mapped[int] = mapped_column(Integer, default=0)
    
    channel = relationship("Channel", back_populates="stats")
    
class StatsTrackEventChannel(Base):
    __tablename__ = "stats_track_event_channel"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_guid: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), db.ForeignKey("stats_track_account_guid.account_guid"), nullable=True)
    channel_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("channel.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now())
    
    channel = relationship("Channel", back_populates="events")
    account_guid_ref = relationship("StatsTrackAccountGuid", back_populates="channel_events")
    
class ChannelCategory(Base):
    __tablename__ = "channel_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    channel_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("channel.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False)

    channel = relationship("Channel", back_populates="categories")
    category = relationship("Category", back_populates="channels")

    channel = relationship("Channel", back_populates="categories")
    category = relationship("Category", back_populates="channels")