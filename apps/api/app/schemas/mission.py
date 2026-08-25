from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import MissionStatus


class MissionBase(BaseModel):
    name: str
    altitude: float | None = None


class MissionCreate(MissionBase):
    organization_id: UUID
    complaint_id: UUID
    pilot_id: UUID | None = None


class MissionUpdate(BaseModel):
    name: str | None = None
    status: MissionStatus | None = None
    altitude: float | None = None


class MissionResponse(MissionBase):
    id: UUID
    organization_id: UUID
    complaint_id: UUID
    pilot_id: UUID | None
    status: MissionStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
