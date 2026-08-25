from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ai.ai_model import AIModel
from app.schemas.ai_model import AIModelCreate


def create(
    db: Session,
    data: AIModelCreate,
):
    model = AIModel(
        **data.model_dump()
    )

    db.add(model)
    db.commit()
    db.refresh(model)

    return model


def get_all(
    db: Session,
):
    return (
        db.query(AIModel)
        .order_by(AIModel.created_at.desc())
        .all()
    )


def get_by_id(
    db: Session,
    model_id: UUID,
):
    return (
        db.query(AIModel)
        .filter(AIModel.id == model_id)
        .first()
    )
