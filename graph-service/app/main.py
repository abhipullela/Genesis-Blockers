from fastapi import FastAPI

from app.api.graph import router as graph_router

app = FastAPI(
    title="Genesis Blockers - Graph Service",
    version="1.0.0",
)

app.include_router(
    graph_router,
    prefix="/api/v1",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "graph-service",
    }