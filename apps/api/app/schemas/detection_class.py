from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DetectionClassCreate(BaseModel):
    name: str
    description: str | None = None
    risk_weight: float = Field(default=1.0, ge=0.0)


class DetectionClassResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    risk_weight: float
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
