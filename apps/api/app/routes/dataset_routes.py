from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.controllers import dataset_controller
from app.database import get_db
from app.schemas.dataset import (
    DatasetCreate,
    DatasetResponse,
)


router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"],
)


@router.post(
    "/",
    response_model=DatasetResponse,
)
def create_dataset(
    data: DatasetCreate,
    db: Session = Depends(get_db),
):
    return dataset_controller.create(
        db,
        data,
    )


@router.get(
    "/",
    response_model=list[DatasetResponse],
)
def list_datasets(
    db: Session = Depends(get_db),
):
    return dataset_controller.get_all(db)


@router.get(
    "/{dataset_id}",
    response_model=DatasetResponse,
)
def get_dataset(
    dataset_id: UUID,
    db: Session = Depends(get_db),
):
    dataset = dataset_controller.get_by_id(
        db,
        dataset_id,
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found",
        )

    return dataset
