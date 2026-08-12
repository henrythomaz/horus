from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import MissionStatus


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    organization_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    complaint_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("complaints.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    pilot_id: Mapped[UUID | None] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    altitude: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    status: Mapped[MissionStatus] = mapped_column(
        SQLEnum(MissionStatus, name="mission_status"),
        nullable=False,
        default=MissionStatus.PLANNED,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    organization = relationship("Organization", back_populates="missions")
    complaint = relationship("Complaint", back_populates="missions")
    pilot = relationship(
        "User",
        back_populates="pilot_missions",
        foreign_keys=[pilot_id],
    )

    images = relationship(
        "Image",
        back_populates="mission",
        cascade="all, delete-orphan",
    )

    risk_areas = relationship(
        "RiskArea",
        back_populates="mission",
        cascade="all, delete-orphan",
    )

    reports = relationship(
        "Report",
        back_populates="mission",
        cascade="all, delete-orphan",
    )
