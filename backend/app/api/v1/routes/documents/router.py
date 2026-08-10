from fastapi import APIRouter
from .docs import DOCUMENTS_TAG

from .upload import router as upload_router

router = APIRouter(
    prefix="/documents",
    tags=[DOCUMENTS_TAG],
)

router.include_router(upload_router)