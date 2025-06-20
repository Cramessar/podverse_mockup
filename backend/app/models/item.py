from sqlalchemy import String, Integer, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.extensions import db
from app.models.base import Base

class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_text: Mapped[Optional[str]] = mapped_column(String(15), unique=True)
    channel_id: Mapped[int] = mapped_column(db.ForeignKey("channel.id"), nullable=False)
    item_flag_status_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey("item_flag_status.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(300))
    slug: Mapped[str] = mapped_column(String(300), unique=True)
    guid:  Mapped[str] = mapped_column(String(300), unique=True)
    guid_enclosure_url:  Mapped[Optional[str]] = mapped_column(String(500), unique=True)
    pub_date: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    
    channel = relationship("Channel", back_populates="items")
    flag_status = relationship("ItemFlagStatus", back_populates="items")
    stats = relationship(
        "StatsAggregatedItem", 
        back_populates="item", 
        cascade="all, delete-orphan"
    )
    events = relationship(
        "StatsTrackEventItem", 
        back_populates="item",
        cascade="all, delete-orphan"
    )

    
class ItemFlagStatus(Base):
    __tablename__ = "item_flag_status"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    items = relationship("Item", back_populates="flag_status")
    
class StatsAggregatedItem(Base):
    __tablename__ = "stats_aggregated_item"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("item.id"), nullable=False)
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
    

    item = relationship("Item", back_populates="stats")

    
class StatsTrackEventItem(Base):
    __tablename__ = "stats_track_event_item"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_guid: Mapped[str] = mapped_column(UUID(as_uuid=False), db.ForeignKey("stats_track_account_guid.account_guid"), nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("item.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now())
    
    
    item = relationship("Item", back_populates="events")
    account_guid_ref = relationship("StatsTrackAccountGuid", back_populates="item_events")
    