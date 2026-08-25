from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ai.prediction import Prediction
from app.schemas.prediction import PredictionCreate


def create(
    db: Session,
    data: PredictionCreate,
) -> Prediction:
    prediction = Prediction(
        **data.model_dump()
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction


def get_by_image(
    db: Session,
    image_id: UUID,
) -> list[Prediction]:
    return (
        db.query(Prediction)
        .filter(
            Prediction.image_id == image_id
        )
        .all()
    )


def get_by_model_run(
    db: Session,
    model_run_id: UUID,
) -> list[Prediction]:
    return (
        db.query(Prediction)
        .filter(
            Prediction.model_run_id == model_run_id
        )
        .all()
    )
