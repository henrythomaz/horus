from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, func
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Prediction(Base):
    __tablename__ = "predictions"
    __table_args__ = (
        CheckConstraint(
            "confidence >= 0 AND confidence <= 1",
            name="ck_prediction_confidence",
        ),
        CheckConstraint("x_center >= 0 AND x_center <= 1", name="ck_prediction_x_center"),
        CheckConstraint("y_center >= 0 AND y_center <= 1", name="ck_prediction_y_center"),
        CheckConstraint("width >= 0 AND width <= 1", name="ck_prediction_width"),
        CheckConstraint("height >= 0 AND height <= 1", name="ck_prediction_height"),
    )

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    image_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("images.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    model_run_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("model_runs.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    class_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("detection_classes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
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

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    image = relationship("Image", back_populates="predictions")
    model_run = relationship("ModelRun", back_populates="predictions")
    detection_class = relationship("DetectionClass", back_populates="predictions")
