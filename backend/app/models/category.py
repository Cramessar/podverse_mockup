from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.extensions import db
from app.models.base import Base

class Category(Base):
    __tablename__ = "category"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, db.ForeignKey("category.id"))
    