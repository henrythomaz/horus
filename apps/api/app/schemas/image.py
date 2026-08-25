from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ImageBase(BaseModel):
    filename: str
    path: str
    latitude: float | None = None
    longitude: float | None = None
    altitude: float | None = None
    captured_at: datetime | None = None
    width: int | None = None
    height: int | None = None
    processed: bool = False


class ImageCreate(ImageBase):
    mission_id: UUID


class ImageResponse(ImageBase):
    id: UUID
    mission_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
