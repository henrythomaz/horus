from sqlalchemy import Column, Integer, String

from .base import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
