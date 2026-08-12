from fastapi import FastAPI

app = FastAPI(
    title="Horus API",
    version="0.1.0",
    description=(
        "Backend do Horus para apoio à detecção de possíveis criadouros "
        "do Aedes aegypti em imagens aéreas."
    ),
)


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
