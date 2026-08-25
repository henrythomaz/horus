from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers import complaint_controller
from app.schemas.complaint import (
    ComplaintCreate,
    ComplaintResponse,
)


router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"],
)


@router.post(
    "/",
    response_model=ComplaintResponse,
)
def create_complaint(
    data: ComplaintCreate,
    db: Session = Depends(get_db),
):

    return complaint_controller.create(
        db,
        data,
    )


@router.get(
    "/",
    response_model=list[ComplaintResponse],
)
def list_complaints(
    db: Session = Depends(get_db),
):

    return complaint_controller.get_all(
        db
    )


@router.get(
    "/{complaint_id}",
    response_model=ComplaintResponse,
)
def get_complaint(
    complaint_id: UUID,
    db: Session = Depends(get_db),
):

    complaint = complaint_controller.get_by_id(
        db,
        complaint_id,
    )

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found",
        )

    return complaint


@router.delete(
    "/{complaint_id}",
)
def delete_complaint(
    complaint_id: UUID,
    db: Session = Depends(get_db),
):

    complaint = complaint_controller.delete(
        db,
        complaint_id,
    )

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found",
        )

    return {
        "message": "deleted"
    }
