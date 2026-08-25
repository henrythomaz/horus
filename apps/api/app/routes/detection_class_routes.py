from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.controllers import detection_class_controller
from app.database import get_db
from app.schemas.detection_class import (
    DetectionClassCreate,
    DetectionClassResponse,
)


router = APIRouter(
    prefix="/detection-classes",
    tags=["Detection Classes"],
)


@router.post(
    "/",
    response_model=DetectionClassResponse,
)
def create_detection_class(
    data: DetectionClassCreate,
    db: Session = Depends(get_db),
):
    return detection_class_controller.create(
        db,
        data,
    )


@router.get(
    "/",
    response_model=list[DetectionClassResponse],
)
def list_detection_classes(
    db: Session = Depends(get_db),
):
    return detection_class_controller.get_all(db)


@router.get(
    "/{class_id}",
    response_model=DetectionClassResponse,
)
def get_detection_class(
    class_id: UUID,
    db: Session = Depends(get_db),
):
    detection_class = (
        detection_class_controller.get_by_id(
            db,
            class_id,
        )
    )

    if not detection_class:
        raise HTTPException(
            status_code=404,
            detail="Detection class not found",
        )

    return detection_class
