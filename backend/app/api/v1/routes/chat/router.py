from fastapi import APIRouter
from .docs import CHAT_TAG

from .ask import router as chat_router

router = APIRouter(
    prefix="/chat",
    tags=[CHAT_TAG],
)

router.include_router(chat_router)