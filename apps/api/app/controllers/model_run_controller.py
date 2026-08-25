from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ai.model_run import ModelRun
from app.schemas.model_run import ModelRunCreate


def create(
    db: Session,
    data: ModelRunCreate,
):
    run = ModelRun(
        **data.model_dump()
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    return run


def get_all(
    db: Session,
):
    return (
        db.query(ModelRun)
        .order_by(
            ModelRun.started_at.desc()
        )
        .all()
    )


def get_by_id(
    db: Session,
    run_id: UUID,
):
    return (
        db.query(ModelRun)
        .filter(
            ModelRun.id == run_id
        )
        .first()
    )
