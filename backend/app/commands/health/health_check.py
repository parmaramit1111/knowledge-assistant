from app.commands import Command
from app.schemas.health import HealthResponse


class HealthCheckCommand(Command[HealthResponse]):

    def execute(self) -> HealthResponse:    
        return HealthResponse(
            status="healthy",
            application=settings.app_name,
            version=settings.app_version,
            environment=settings.app_env,
        )