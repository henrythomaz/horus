from .organization_routes import router as organization_router
from .user_routes import router as user_router
from .complaint_routes import router as complaint_router
from .missions_routes import router as mission_router
from .images_routes import router as image_router
from .predictions_routes import router as prediction_router

from .dataset_routes import router as dataset_router
from .ai_model_routes import router as ai_model_router
from .model_run_routes import router as model_run_router
from .detection_class_routes import router as detection_class_router


__all__ = [
    "organization_router",
    "user_router",
    "complaint_router",
    "mission_router",
    "image_router",
    "prediction_router",
    "dataset_router",
    "ai_model_router",
    "model_run_router",
    "detection_class_router",
]
