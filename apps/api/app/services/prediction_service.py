from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ai.detection_class import DetectionClass
from app.models.ai.prediction import Prediction


def get_class_id(
    db: Session,
    class_index,
    model,
):
    class_index = int(class_index)

    class_name = model.names[class_index]

    detection = (
        db.query(DetectionClass)
        .filter(
            DetectionClass.name == class_name
        )
        .first()
    )

    if not detection:
        raise ValueError(
            f"Detection class '{class_name}' "
            "not found in database"
        )

    return detection.id


def save_predictions(
    db: Session,
    image_id: UUID,
    model_run_id: UUID,
    results,
    model,
):
    predictions = []

    for result in results:
        for box in result.boxes:
            prediction = Prediction(
                image_id=image_id,
                model_run_id=model_run_id,
                class_id=get_class_id(
                    db=db,
                    class_index=box.cls[0],
                    model=model,
                ),
                confidence=float(
                    box.conf[0]
                ),
                x_center=float(
                    box.xywhn[0][0]
                ),
                y_center=float(
                    box.xywhn[0][1]
                ),
                width=float(
                    box.xywhn[0][2]
                ),
                height=float(
                    box.xywhn[0][3]
                ),
            )

            db.add(prediction)
            predictions.append(prediction)

    db.flush()

    return predictions
