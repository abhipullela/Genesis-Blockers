from fastapi import FastAPI

from app.api.scoring import router


app = FastAPI(
    title="Confidence & Risk Scoring Service",
    version="0.1.0",
)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "healthy"}