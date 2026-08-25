from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers import organization_controller
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
)


router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.post(
    "/",
    response_model=OrganizationResponse,
)
def create_organization(
    data: OrganizationCreate,
    db: Session = Depends(get_db),
):
    return organization_controller.create(
        db,
        data,
    )


@router.get(
    "/",
    response_model=list[OrganizationResponse],
)
def list_organizations(
    db: Session = Depends(get_db),
):
    return organization_controller.get_all(db)


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def get_organization(
    organization_id: UUID,
    db: Session = Depends(get_db),
):

    organization = organization_controller.get_by_id(
        db,
        organization_id,
    )

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found",
        )

    return organization
