from fastapi import APIRouter

from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.documents.router import router as upload_router
from app.api.v1.routes.search.router import router as search_router
from app.api.v1.routes.chat.router import router as chat_router


router = APIRouter(prefix="/v1")

router.include_router(health_router)
router.include_router(upload_router)
router.include_router(search_router)
router.include_router(chat_router)