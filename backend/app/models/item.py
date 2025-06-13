from sqlalchemy import String, DateTime
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
    