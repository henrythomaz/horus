from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import DatasetSplit


class DatasetImage(Base):
    __tablename__ = "dataset_images"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    dataset_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    filename: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    path: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    split: Mapped[DatasetSplit] = mapped_column(
        SQLEnum(DatasetSplit, name="dataset_split"),
        nullable=False,
        index=True,
    )

    width: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    height: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    dataset = relationship("Dataset", back_populates="images")

    annotations = relationship(
        "DatasetAnnotation",
        back_populates="dataset_image",
        cascade="all, delete-orphan",
    )
