from fastapi import FastAPI

from app.routes import (
    organization_router,
    user_router,
    complaint_router,
    mission_router,
    image_router,
    prediction_router,
    dataset_router,
    ai_model_router,
    model_run_router,
    detection_class_router,
)


app = FastAPI(
    title="Horus API",
    version="0.1.0",
    description=(
        "Backend do Horus para análise "
        "de imagens aéreas e detecção "
        "de criadouros do Aedes aegypti."
    ),
)


app.include_router(organization_router)
app.include_router(user_router)
app.include_router(complaint_router)
app.include_router(mission_router)
app.include_router(image_router)
app.include_router(prediction_router)

app.include_router(dataset_router)
app.include_router(ai_model_router)
app.include_router(model_run_router)
app.include_router(detection_class_router)


@app.get("/")
def root():
    return {
        "project": "Horus",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }
