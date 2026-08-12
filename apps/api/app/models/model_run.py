from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, JSON
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ModelRun(Base):
    __tablename__ = "model_runs"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    model_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("models.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    dataset_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("datasets.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    metrics: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    model = relationship("AIModel", back_populates="model_runs")
    dataset = relationship("Dataset", back_populates="model_runs")

    predictions = relationship(
        "Prediction",
        back_populates="model_run",
    )
