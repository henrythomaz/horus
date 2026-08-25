from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import ModelTask


class AIModelCreate(BaseModel):
    name: str
    version: str
    task: ModelTask
    path: str


class AIModelResponse(BaseModel):
    id: UUID
    name: str
    version: str
    task: ModelTask
    path: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
