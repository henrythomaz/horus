from uuid import UUID

from sqlalchemy.orm import Session

from app.models.operational.complaint import Complaint
from app.schemas.complaint import ComplaintCreate


def create(
    db: Session,
    data: ComplaintCreate
):

    complaint = Complaint(
        **data.model_dump()
    )

    db.add(complaint)
    db.commit()
    db.refresh(complaint)

    return complaint


def get_all(
    db: Session
):

    return (
        db.query(Complaint)
        .all()
    )


def get_by_id(
    db: Session,
    complaint_id: UUID
):

    return (
        db.query(Complaint)
        .filter(
            Complaint.id == complaint_id
        )
        .first()
    )


def delete(
    db: Session,
    complaint_id: UUID
):

    complaint = get_by_id(
        db,
        complaint_id
    )

    if complaint:
        db.delete(complaint)
        db.commit()

    return complaint
