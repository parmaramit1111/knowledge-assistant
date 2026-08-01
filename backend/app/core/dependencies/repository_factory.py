from app.repositories.document_repository import DocumentRepository
from app.repositories.parsed_document_repository import ParsedDocumentRepository

class RepositoryFactory:

    @staticmethod
    def document_repository():
        return DocumentRepository()

    @staticmethod
    def parsed_document_repository():
        return ParsedDocumentRepository()
