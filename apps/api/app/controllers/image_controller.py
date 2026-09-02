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


def create_many(
    db: Session,
    mission_id: UUID,
    images_data: list[dict],
):
    images = [
        Image(
            mission_id=mission_id,
            filename=data["filename"],
            path=data["path"],
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            altitude=data.get("altitude"),
            processing_status="pending",
        )
        for data in images_data
    ]

    db.add_all(images)
    db.commit()

    for image in images:
        db.refresh(image)

    return images
