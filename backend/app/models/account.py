from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.extensions import db
from app.models.base import Base

class Account(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sharable_status_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey("sharable_status.id"), nullable=True)
    verified: Mapped[bool] = mapped_column(db.Boolean, default=False)
    id_text: Mapped[Optional[str]] = mapped_column(String(15), unique=True)
    
class SharableStatus(Base):
    __tablename__ = "sharable_status"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(50))