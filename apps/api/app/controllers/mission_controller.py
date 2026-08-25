from uuid import UUID

from sqlalchemy.orm import Session

from app.models.operational.mission import Mission
from app.schemas.mission import MissionCreate


def create(
    db: Session,
    data: MissionCreate
):

    mission = Mission(
        **data.model_dump()
    )

    db.add(mission)
    db.commit()
    db.refresh(mission)

    return mission



def get_all(
    db: Session
):

    return (
        db.query(Mission)
        .all()
    )



def get_by_id(
    db: Session,
    mission_id: UUID
):

    return (
        db.query(Mission)
        .filter(
            Mission.id == mission_id
        )
        .first()
    )
