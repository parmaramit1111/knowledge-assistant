from app.repositories.document_repository import DocumentRepository

class RepositoryFactory:

    @staticmethod
    def document_repository():
        return DocumentRepository()