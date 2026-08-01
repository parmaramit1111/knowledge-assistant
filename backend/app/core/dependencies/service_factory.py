from app.services.document_upload_service import DocumentUploadService
from app.queries.health.health_check import HealthCheckQuery

class ServiceFactory:

    @staticmethod
    def document_service():
        return DocumentUploadService()

    @staticmethod
    def get_health_check_query() -> HealthCheckQuery:
        return HealthCheckQuery()