from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.extensions import db
from app.models.base import Base

class Account(Base):
    __tablename__ = "account"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sharable_status_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey("sharable_status.id"), nullable=True)
    verified: Mapped[bool] = mapped_column(db.Boolean, default=False)
    id_text: Mapped[Optional[str]] = mapped_column(String(15), unique=True)
    
    sharable_status = relationship("SharableStatus", back_populates="accounts")
    guid_tracking = relationship(
        "StatsTrackAccountGuid", 
        back_populates="account",
        cascade="all, delete-orphan"
    )
    
class SharableStatus(Base):
    __tablename__ = "sharable_status"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(50))
    
    accounts = relationship("Account", back_populates="sharable_status")
    
class StatsTrackAccountGuid(Base):
    __tablename__ = "stats_track_account_guid"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("account.id"), nullable=False)
    account_guid: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    account = relationship("Account", back_populates="guid_tracking")
    channel_events = relationship("StatsTrackEventChannel", back_populates="account_guid_ref")
    item_events = relationship("StatsTrackEventItem", back_populates="account_guid_ref")