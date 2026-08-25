from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers import mission_controller
from app.schemas.mission import (
    MissionCreate,
    MissionResponse,
)


router = APIRouter(
    prefix="/missions",
    tags=["Missions"],
)



@router.post(
    "/",
    response_model=MissionResponse,
)
def create_mission(
    data: MissionCreate,
    db: Session = Depends(get_db),
):

    return mission_controller.create(
        db,
        data,
    )



@router.get(
    "/",
    response_model=list[MissionResponse],
)
def list_missions(
    db: Session = Depends(get_db),
):

    return mission_controller.get_all(
        db
    )



@router.get(
    "/{mission_id}",
    response_model=MissionResponse,
)
def get_mission(
    mission_id: UUID,
    db: Session = Depends(get_db),
):

    mission = mission_controller.get_by_id(
        db,
        mission_id,
    )

    if not mission:
        raise HTTPException(
            status_code=404,
            detail="Mission not found",
        )

    return mission
