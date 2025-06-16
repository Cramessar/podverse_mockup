from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.extensions import db
from app.models.base import Base

class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_text: Mapped[Optional[str]] = mapped_column(String(15), unique=True)
    channel_id: Mapped[int] = mapped_column(db.ForeignKey("channel.id"), nullable=False)
    #item_flag_status_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey("item_flag_status.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(300))
    slug: Mapped[str] = mapped_column(String(300), unique=True)
    guid:  Mapped[str] = mapped_column(String(300), unique=True)
    guid_enclosure_url:  Mapped[Optional[str]] = mapped_column(String(500), unique=True)
    published_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    
class ItemFlagStatus(Base):
    __tablename__ = "item_flag_status"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
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
    