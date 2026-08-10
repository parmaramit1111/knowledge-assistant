from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.queries.health.health_check import HealthCheckQuery

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse)
def health() -> HealthResponse:
    """
    Return the health status of the application.
    """
    health_check = HealthCheckQuery()
    return health_check.execute()