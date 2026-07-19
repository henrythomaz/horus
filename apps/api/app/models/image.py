from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Image(Base):
    __tablename__ = "images"

    id:  Mapped[int] = mapped_column(primary_key=True)
    
    filename: Mapped[str] = mapped_column(String(255))

