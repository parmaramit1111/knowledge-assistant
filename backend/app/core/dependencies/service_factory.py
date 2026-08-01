from app.queries.health.health_check import HealthCheckQuery
from app.services.document_upload_service import DocumentUploadService
from app.services.document_processing_service import DocumentProcessingService


class ServiceFactory:

    @staticmethod
    def get_health_check_query() -> HealthCheckQuery:
        return HealthCheckQuery()

    @staticmethod
    def document_service():
        return DocumentUploadService()

    @staticmethod
    def document_processing_service():
        return DocumentProcessingService()