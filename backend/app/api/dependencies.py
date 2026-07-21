from app.queries.health.health_check import HealthCheckQuery


def get_health_check_query() -> HealthCheckQuery:
    return HealthCheckQuery()