from app.queries.health.health_check import HealthCheckQuery
from app.services.document_upload_service import DocumentUploadService

def get_health_check_query() -> HealthCheckQuery:
    return HealthCheckQuery()

def get_document_upload_service() -> DocumentUploadService:
    return DocumentUploadService()