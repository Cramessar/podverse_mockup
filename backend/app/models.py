from sqlalchemy import Column, Integer, String
from database import Base

class Podcast(Base):
    __tablename__ = "podcasts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    publisher = Column(String, index=True)
    category = Column(String, index=True)
