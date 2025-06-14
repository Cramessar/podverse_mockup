from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.extensions import db
from app.models.base import Base

class Feed(Base):
    __tablename__ = "feed"

    id: Mapped[int] = mapped_column(primary_key=True)
    #feed_flag_status_id: Mapped[int] = mapped_column(db.ForeignKey("feed_flag_status.id"))
    url: Mapped[str] = mapped_column(String(300), unique=True)
    last_parsed: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=db.func.now(), onupdate=db.func.now())
    # set to time when parsing starts and NULL when parsing ends
    is_parsing: Mapped[Optional[DateTime]] = mapped_column(DateTime)