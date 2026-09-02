import os
from datetime import datetime, timezone
from uuid import UUID

from app.database import SessionLocal
from app.models.ai.ai_model import AIModel
from app.models.ai.dataset import Dataset
from app.models.ai.model_run import ModelRun
from app.models.operational.image import Image

from app.services.ai_service import (
    load_model,
    predict_batch,
)

from app.services.annotation_service import (
    create_annotated_image,
)

from app.services.prediction_service import (
    save_predictions_batch,
)


YOLO_BATCH_SIZE = int(
    os.getenv(
        "YOLO_BATCH_SIZE",
        "4",
    )
)


def chunks(items, size):
    for i in range(
        0,
        len(items),
        size,
    ):
        yield items[
            i:i + size
        ]


def process_image_batch(
    image_ids: list[str],
):
    db = SessionLocal()

    ids = [
        UUID(image_id)
        for image_id in image_ids
    ]

    try:
        images = (
            db.query(Image)
            .filter(
                Image.id.in_(ids)
            )
            .all()
        )

        if len(images) != len(ids):
            raise ValueError(
                "One or more images were not found"
            )

        image_by_id = {
            image.id: image
            for image in images
        }

        ordered_images = [
            image_by_id[image_id]
            for image_id in ids
        ]

        # Início

        for image in ordered_images:
            image.processing_status = "processing"
            image.processing_error = None

        db.commit()

        # Modelo

        ai_model = (
            db.query(AIModel)
            .order_by(
                AIModel.created_at.desc()
            )
            .first()
        )

        if not ai_model:
            raise RuntimeError(
                "AI Model not registered"
            )

        # Dataset

        dataset = (
            db.query(Dataset)
            .order_by(
                Dataset.created_at.desc()
            )
            .first()
        )

        if not dataset:
            raise RuntimeError(
                "Dataset not registered"
            )

        # YOLO

        model = load_model()

        # Model Run

        run = ModelRun(
            model_id=ai_model.id,
            dataset_id=dataset.id,
            started_at=datetime.now(
                timezone.utc
            ),
        )

        db.add(run)
        db.commit()
        db.refresh(run)

        total_predictions = 0

        # Processa os batches

        for image_chunk in chunks(
            ordered_images,
            YOLO_BATCH_SIZE,
        ):
            paths = [
                image.path
                for image in image_chunk
            ]

            results = predict_batch(
                paths,
                batch_size=YOLO_BATCH_SIZE,
            )

            if len(results) != len(
                image_chunk
            ):
                raise RuntimeError(
                    "YOLO returned an unexpected "
                    "number of results"
                )

            predictions = (
                save_predictions_batch(
                    db=db,
                    images=image_chunk,
                    model_run_id=run.id,
                    results=results,
                    model=model,
                )
            )

            total_predictions += len(
                predictions
            )

            # Finaliza somente este chunk

            for image, result in zip(
                image_chunk,
                results,
            ):
                create_annotated_image(
                    image.path,
                    [result],
                )

                image.processed = True
                image.processing_status = (
                    "completed"
                )
                image.processing_error = None

            db.commit()

        # Finaliza ModelRun

        run.finished_at = datetime.now(
            timezone.utc
        )

        run.metrics = {
            "images": len(ordered_images),
            "predictions": total_predictions,
            "batch_size": YOLO_BATCH_SIZE,
        }

        db.commit()

        return {
            "images": len(ordered_images),
            "predictions": total_predictions,
        }

    except Exception as exc:
        db.rollback()

        # Marca como failed apenas as imagens que
        # ainda não foram concluídas.
        failed_images = (
            db.query(Image)
            .filter(
                Image.id.in_(ids),
                Image.processing_status != "completed",
            )
            .all()
        )

        for image in failed_images:
            image.processing_status = "failed"
            image.processing_error = str(exc)

        db.commit()

        raise

    finally:
        db.close()
