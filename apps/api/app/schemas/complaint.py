from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import ComplaintStatus


class ComplaintBase(BaseModel):
    description: str
    neighborhood: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class ComplaintCreate(ComplaintBase):
    organization_id: UUID
    reported_by: UUID


class ComplaintResponse(ComplaintBase):
    id: UUID
    organization_id: UUID
    reported_by: UUID
    status: ComplaintStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
