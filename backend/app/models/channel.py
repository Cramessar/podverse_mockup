from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.extensions import db
from app.models.base import Base  

class Channel(Base):
    __tablename__ = "channel"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_text: Mapped[Optional[str]] = mapped_column(String(15), unique=True)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(2500))
    publisher: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    status: Mapped[Optional[str]] = mapped_column(String(50))
    status_since: Mapped[Optional[DateTime]] = mapped_column(DateTime)
