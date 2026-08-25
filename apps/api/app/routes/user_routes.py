from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers import user_controller
from app.schemas.user import (
    UserCreate,
    UserResponse,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponse,
)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):

    return user_controller.create(
        db,
        data,
    )


@router.get(
    "/",
    response_model=list[UserResponse],
)
def list_users(
    db: Session = Depends(get_db),
):

    return user_controller.get_all(db)
