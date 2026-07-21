from app.core.config import settings
from app.queries import Query
from app.schemas.health import HealthResponse


class HealthCheckQuery(Query[HealthResponse]):

    def execute(self) -> HealthResponse:
        return HealthResponse(
            status="healthy",
            application=settings.app_name,
            version=settings.app_version,
            environment=settings.app_env,
        )