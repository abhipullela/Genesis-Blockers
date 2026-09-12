from fastapi import FastAPI

from app.routes import router

app = FastAPI(
    title="VASP Intelligence Service"
)

app.include_router(
    router,
    prefix="/api/v1"
)


@app.get("/")
def root():
    return {
        "message": "VASP Intelligence Service is running"
    }