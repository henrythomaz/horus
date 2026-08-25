from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DatasetCreate(BaseModel):
    name: str
    version: str
    description: str | None = None


class DatasetResponse(BaseModel):
    id: UUID
    name: str
    version: str
    description: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
