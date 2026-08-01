from fastapi import APIRouter

from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.documents.upload import router as upload_router

router = APIRouter(prefix="/v1")

router.include_router(health_router)
router.include_router(upload_router)