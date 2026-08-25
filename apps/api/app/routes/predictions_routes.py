from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.controllers import prediction_controller
from app.database import get_db
from app.schemas.prediction import (
    PredictionCreate,
    PredictionResponse,
)


router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


@router.post(
    "/",
    response_model=PredictionResponse,
)
def create_prediction(
    data: PredictionCreate,
    db: Session = Depends(get_db),
):
    return prediction_controller.create(
        db,
        data,
    )


@router.get(
    "/image/{image_id}",
    response_model=list[PredictionResponse],
)
def list_predictions_by_image(
    image_id: UUID,
    db: Session = Depends(get_db),
):
    predictions = prediction_controller.get_by_image(
        db,
        image_id,
    )

    if not predictions:
        raise HTTPException(
            status_code=404,
            detail="No predictions for this image",
        )

    return predictions


@router.get(
    "/model-run/{model_run_id}",
    response_model=list[PredictionResponse],
)
def list_predictions_by_model_run(
    model_run_id: UUID,
    db: Session = Depends(get_db),
):
    predictions = (
        prediction_controller.get_by_model_run(
            db,
            model_run_id,
        )
    )

    if not predictions:
        raise HTTPException(
            status_code=404,
            detail="No predictions for this model run",
        )

    return predictions
