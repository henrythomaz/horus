from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ModelRunCreate(BaseModel):
    model_id: UUID
    dataset_id: UUID
    started_at: datetime
    finished_at: datetime | None = None
    metrics: dict[str, Any] | None = None


class ModelRunResponse(BaseModel):
    id: UUID
    model_id: UUID
    dataset_id: UUID
    started_at: datetime
    finished_at: datetime | None
    metrics: dict[str, Any] | None

    model_config = ConfigDict(
        from_attributes=True
    )
