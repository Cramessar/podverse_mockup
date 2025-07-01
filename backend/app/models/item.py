# backend/app/models/item.py

from sqlalchemy import Integer, String, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.extensions import db
from app.models.base import Base
from app.models.stats import StatsAggregatedItem, StatsTrackEventItem


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_text: Mapped[Optional[str]] = mapped_column(String(15), unique=True)
    channel_id: Mapped[int] = mapped_column(db.ForeignKey("channel.id"), nullable=False)
    item_flag_status_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey("item_flag_status.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(300))
    slug: Mapped[str] = mapped_column(String(300), unique=True)
    guid: Mapped[str] = mapped_column(String(300), unique=True)
    guid_enclosure_url: Mapped[Optional[str]] = mapped_column(String(500), unique=True)
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
