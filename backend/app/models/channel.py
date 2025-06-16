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
