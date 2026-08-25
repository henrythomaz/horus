from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers import image_controller
from app.models.ai.ai_model import AIModel
from app.models.ai.dataset import Dataset
from app.models.ai.model_run import ModelRun
from app.models.ai.prediction import Prediction
from app.models.operational.image import Image
from app.services.ai_service import load_model, predict
from app.services.annotation_service import create_annotated_image
from app.services.image_service import save_image
from app.services.prediction_service import save_predictions


router = APIRouter(
    prefix="/images",
    tags=["Images"],
)


@router.post("/{mission_id}")
def upload_image(
    mission_id: UUID,
    file: UploadFile = File(...),
    latitude: float | None = Form(None),
    longitude: float | None = Form(None),
    altitude: float | None = Form(None),
    db: Session = Depends(get_db),
):
    path = save_image(file)

    image = image_controller.create(
        db,
        mission_id=mission_id,
        filename=file.filename or "unknown",
        path=path,
        latitude=latitude,
        longitude=longitude,
        altitude=altitude,
    )

    return image


@router.post("/{image_id}/process")
def process_image(
    image_id: UUID,
    db: Session = Depends(get_db),
):
    # 1. Busca a imagem
    image = (
        db.query(Image)
        .filter(Image.id == image_id)
        .first()
    )

    if not image:
        raise HTTPException(
            status_code=404,
            detail="Image not found",
        )

    # 2. Busca o modelo cadastrado
    ai_model = (
        db.query(AIModel)
        .order_by(AIModel.created_at.desc())
        .first()
    )

    if not ai_model:
        raise HTTPException(
            status_code=500,
            detail="AI Model not registered",
        )

    # 3. Busca o dataset associado ao modelo
    dataset = (
        db.query(Dataset)
        .order_by(Dataset.created_at.desc())
        .first()
    )

    if not dataset:
        raise HTTPException(
            status_code=500,
            detail="Dataset not registered",
        )

    # 4. Carrega o modelo YOLO
    try:
        model = load_model()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not load AI model: {exc}",
        ) from exc

    # 5. Cria o registro da execução
    run = ModelRun(
        model_id=ai_model.id,
        dataset_id=dataset.id,
        started_at=datetime.now(timezone.utc),
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    try:
        # 6. Executa a inferência
        results = predict(
            image.path
        )

        # 7. Salva as predictions
        predictions = save_predictions(
            db=db,
            image_id=image.id,
            model_run_id=run.id,
            results=results,
            model=model,
        )

        # 8. Gera a imagem anotada
        annotated_path = create_annotated_image(
            image.path,
            results,
        )

        # 9. Marca imagem como processada
        image.processed = True

        # 10. Finaliza a execução
        run.finished_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(image)
        db.refresh(run)

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Image processing failed: {exc}",
        ) from exc

    return {
        "image_id": str(image.id),
        "model_run_id": str(run.id),
        "detections": len(predictions),
        "annotated_image": (
            f"/images/{image.id}/result/image"
        ),
    }


@router.get("/{image_id}/result")
def image_result(
    image_id: UUID,
    db: Session = Depends(get_db),
):
    image = (
        db.query(Image)
        .filter(Image.id == image_id)
        .first()
    )

    if not image:
        raise HTTPException(
            status_code=404,
            detail="Image not found",
        )

    predictions = (
        db.query(Prediction)
        .filter(
            Prediction.image_id == image_id
        )
        .all()
    )

    return {
        "image_id": str(image.id),
        "mission_id": str(image.mission_id),
        "original_image": image.path,
        "processed": image.processed,
        "detections": [
            {
                "id": str(prediction.id),
                "class_id": str(prediction.class_id),
                "model_run_id": str(prediction.model_run_id),
                "confidence": prediction.confidence,
                "x_center": prediction.x_center,
                "y_center": prediction.y_center,
                "width": prediction.width,
                "height": prediction.height,
            }
            for prediction in predictions
        ],
    }


@router.get("/{image_id}/result/image")
def get_annotated_image(
    image_id: UUID,
    db: Session = Depends(get_db),
):
    image = (
        db.query(Image)
        .filter(Image.id == image_id)
        .first()
    )

    if not image:
        raise HTTPException(
            status_code=404,
            detail="Image not found",
        )

    original_path = Path(image.path)

    annotated_path = (
        Path("storage/processed")
        / original_path.name
    )

    if not annotated_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Processed image not found. Process the image first.",
        )

    return FileResponse(
        path=annotated_path,
        media_type="image/jpeg",
        filename=annotated_path.name,
    )
