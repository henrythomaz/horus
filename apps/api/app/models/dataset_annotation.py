from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Float, ForeignKey
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class DatasetAnnotation(Base):
    __tablename__ = "dataset_annotations"
    __table_args__ = (
        CheckConstraint("x_center >= 0 AND x_center <= 1", name="ck_annotation_x_center"),
        CheckConstraint("y_center >= 0 AND y_center <= 1", name="ck_annotation_y_center"),
        CheckConstraint("width >= 0 AND width <= 1", name="ck_annotation_width"),
        CheckConstraint("height >= 0 AND height <= 1", name="ck_annotation_height"),
    )

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    dataset_image_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("dataset_images.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    class_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("detection_classes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    x_center: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    y_center: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    width: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    height: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    dataset_image = relationship("DatasetImage", back_populates="annotations")
    detection_class = relationship(
        "DetectionClass",
        back_populates="dataset_annotations",
    )
