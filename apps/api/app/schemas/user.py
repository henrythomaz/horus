from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from app.models.enums import UserRole


class UserCreate(BaseModel):

    organization_id: UUID
    name: str
    email: str
    password_hash: str
    role: UserRole = UserRole.AGENT



class UserResponse(BaseModel):

    id: UUID
    organization_id: UUID
    name: str
    email: str
    role: UserRole
    created_at: datetime


    class Config:
        from_attributes = True
