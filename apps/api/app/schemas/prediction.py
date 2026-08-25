from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PredictionBase(BaseModel):
    confidence: float = Field(..., ge=0.0, le=1.0)
    x_center: float = Field(..., ge=0.0, le=1.0)
    y_center: float = Field(..., ge=0.0, le=1.0)
    width: float = Field(..., ge=0.0, le=1.0)
    height: float = Field(..., ge=0.0, le=1.0)


class PredictionCreate(PredictionBase):
    image_id: UUID
    model_run_id: UUID
    class_id: UUID


class PredictionResponse(PredictionBase):
    id: UUID
    image_id: UUID
    model_run_id: UUID
    class_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
