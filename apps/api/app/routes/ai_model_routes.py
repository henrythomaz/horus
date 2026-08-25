from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.controllers import ai_model_controller
from app.database import get_db
from app.schemas.ai_model import (
    AIModelCreate,
    AIModelResponse,
)


router = APIRouter(
    prefix="/models",
    tags=["AI Models"],
)


@router.post(
    "/",
    response_model=AIModelResponse,
)
def create_model(
    data: AIModelCreate,
    db: Session = Depends(get_db),
):
    return ai_model_controller.create(
        db,
        data,
    )


@router.get(
    "/",
    response_model=list[AIModelResponse],
)
def list_models(
    db: Session = Depends(get_db),
):
    return ai_model_controller.get_all(db)


@router.get(
    "/{model_id}",
    response_model=AIModelResponse,
)
def get_model(
    model_id: UUID,
    db: Session = Depends(get_db),
):
    model = ai_model_controller.get_by_id(
        db,
        model_id,
    )

    if not model:
        raise HTTPException(
            status_code=404,
            detail="AI Model not found",
        )

    return model
