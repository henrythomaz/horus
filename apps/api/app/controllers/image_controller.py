from uuid import UUID

from sqlalchemy.orm import Session

from app.models.operational.image import Image


def create(
    db: Session,
    mission_id: UUID,
    filename: str,
    path: str,
    latitude: float | None = None,
    longitude: float | None = None,
    altitude: float | None = None,
):
    image = Image(
        mission_id=mission_id,
        filename=filename,
        path=path,
        latitude=latitude,
        longitude=longitude,
        altitude=altitude,
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return image


def get_by_mission(
    db: Session,
    mission_id: UUID,
):
    return (
        db.query(Image)
        .filter(
            Image.mission_id == mission_id
        )
        .all()
    )
