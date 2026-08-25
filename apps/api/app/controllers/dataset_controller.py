from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ai.dataset import Dataset
from app.schemas.dataset import DatasetCreate


def create(
    db: Session,
    data: DatasetCreate,
):
    dataset = Dataset(
        **data.model_dump()
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return dataset


def get_all(
    db: Session,
):
    return (
        db.query(Dataset)
        .order_by(
            Dataset.created_at.desc()
        )
        .all()
    )


def get_by_id(
    db: Session,
    dataset_id: UUID,
):
    return (
        db.query(Dataset)
        .filter(
            Dataset.id == dataset_id
        )
        .first()
    )
