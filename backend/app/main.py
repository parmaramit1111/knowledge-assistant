from fastapi import FastAPI

from app.api.router import router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}"
    }