from fastapi import FastAPI

from app.api.routes.investigate import router as investigate_router

from app.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


app.include_router(
    investigate_router,
    prefix="/api/v1",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }