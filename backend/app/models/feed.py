from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.extensions import db
from app.models.base import Base

class Feed(Base):
    __tablename__ = "feed"

    id: Mapped[int] = mapped_column(primary_key=True)
    feed_flag_status_id: Mapped[int] = mapped_column(db.ForeignKey("feed_flag_status.id"))
    url: Mapped[str] = mapped_column(String(2083), unique=True)
    last_parsed_file_hash: Mapped[Optional[str]] = mapped_column(String(32))
    parsing_priority: Mapped[int] = mapped_column(Integer, default=0)
    container_id: Mapped[Optional[str]] = mapped_column(String(12))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now(), onupdate=db.func.now())
    # set to true when parsing starts and false when parsing ends
    # In db schema, is_parsing is BOOLEAN DEFAULT false and nullable = YES.
    is_parsing: Mapped[bool] = mapped_column(db.Boolean, default=False)

    
    flag_status = relationship("FeedFlagStatus", back_populates="feeds")
    channels = relationship("Channel", back_populates="feed")
    logs = relationship(
        "FeedLog", 
        back_populates="feed",
        cascade="all, delete-orphan"
    )
    
class FeedFlagStatus(Base):
    __tablename__ = "feed_flag_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now(), onupdate=db.func.now())
    status: Mapped[str] = mapped_column(String(50))
    
    feeds = relationship("Feed", back_populates="flag_status")
    
class FeedLog(Base):
    __tablename__ = "feed_log"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    feed_id: Mapped[int] = mapped_column(db.ForeignKey("feed.id"))
    last_http_status: Mapped[Optional[int]] = mapped_column(db.Integer)
    last_good_http_status_time: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    last_finished_parse_time: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    parse_errors: Mapped[Optional[int]] = mapped_column(db.Integer, default=0)
    
    feed = relationship("Feed", back_populates="logs")