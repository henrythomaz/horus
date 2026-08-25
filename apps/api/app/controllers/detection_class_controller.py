from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ai.detection_class import DetectionClass
from app.schemas.detection_class import DetectionClassCreate


def create(
    db: Session,
    data: DetectionClassCreate,
):
    detection_class = DetectionClass(
        **data.model_dump()
    )

    db.add(detection_class)
    db.commit()
    db.refresh(detection_class)

    return detection_class


def get_all(
    db: Session,
):
    return (
        db.query(DetectionClass)
        .order_by(
            DetectionClass.name
        )
        .all()
    )


def get_by_id(
    db: Session,
    class_id: UUID,
):
    return (
        db.query(DetectionClass)
        .filter(
            DetectionClass.id == class_id
        )
        .first()
    )
