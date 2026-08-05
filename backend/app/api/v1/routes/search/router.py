from fastapi import APIRouter
from .docs import QUERY_TAG

from .query import router as query_router

router = APIRouter(
    prefix="/search",
    tags=[QUERY_TAG],
)

router.include_router(query_router)