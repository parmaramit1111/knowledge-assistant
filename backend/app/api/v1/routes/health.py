from fastapi import APIRouter, Depends

from app.core.dependencies.service_factory import ServiceFactory
from app.queries.health.health_check import HealthCheckQuery
from app.schemas.health import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse)
def health(
    query: HealthCheckQuery = Depends(ServiceFactory.get_health_check_query),
) -> HealthResponse:
    return query.execute()