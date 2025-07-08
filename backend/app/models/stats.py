# backend/app/models/stats.py

from sqlalchemy import Integer, ForeignKey, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from app.models.base import Base


class StatsAggregatedChannel(Base):
    __tablename__ = "stats_aggregated_channel"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"), nullable=False)

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


class StatsAggregatedItem(Base):
    __tablename__ = "stats_aggregated_item"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), nullable=False)

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
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), nullable=False)
    account_guid: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("stats_track_account_guid.account_guid"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now())

    item = relationship("Item", back_populates="events")
    account_guid_ref = relationship("StatsTrackAccountGuid", back_populates="item_events")


class StatsTrackEventChannel(Base):
    __tablename__ = "stats_track_event_channel"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"), nullable=False)
    account_guid: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("stats_track_account_guid.account_guid"), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now())

    channel = relationship("Channel", back_populates="events")
    account_guid_ref = relationship("StatsTrackAccountGuid", back_populates="channel_events")
