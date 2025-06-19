from sqlalchemy import Integer, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Medium(Base):
    __tablename__ = "medium"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[str] = mapped_column(Text, 
        CheckConstraint(
            "value IN ("
            "'publisher','podcast','music','video','film','audiobook',"
            "'newsletter','blog','course','mixed',"
            "'podcastL','musicL','videoL','filmL','audiobookL',"
            "'newsletterL','blogL','publisherL','courseL'"
            ")",
            name="ck_medium_value",
        ),
    )
    
    channels = relationship("Channel", back_populates="medium")