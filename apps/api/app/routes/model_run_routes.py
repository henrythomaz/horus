from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.controllers import model_run_controller
from app.database import get_db
from app.schemas.model_run import (
    ModelRunCreate,
    ModelRunResponse,
)


router = APIRouter(
    prefix="/model-runs",
    tags=["Model Runs"],
)


@router.post(
    "/",
    response_model=ModelRunResponse,
)
def create_model_run(
    data: ModelRunCreate,
    db: Session = Depends(get_db),
):
    return model_run_controller.create(
        db,
        data,
    )


@router.get(
    "/",
    response_model=list[ModelRunResponse],
)
def list_model_runs(
    db: Session = Depends(get_db),
):
    return model_run_controller.get_all(db)


@router.get(
    "/{run_id}",
    response_model=ModelRunResponse,
)
def get_model_run(
    run_id: UUID,
    db: Session = Depends(get_db),
):
    run = model_run_controller.get_by_id(
        db,
        run_id,
    )

    if not run:
        raise HTTPException(
            status_code=404,
            detail="Model run not found",
        )

    return run
