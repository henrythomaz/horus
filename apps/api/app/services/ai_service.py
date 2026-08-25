from pathlib import Path

from ultralytics import YOLO


MODEL_PATH = Path("models/best2.pt")

_model = None


def load_model():
    global _model

    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"AI model not found at: {MODEL_PATH}"
            )

        _model = YOLO(
            str(MODEL_PATH)
        )

    return _model


def predict(
    image_path: str,
):
    model = load_model()

    return model(
        image_path
    )
