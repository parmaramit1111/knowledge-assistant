from uuid import UUID

from app.models.document import (
    ChunkStatus,
    Document,
    DocumentStatus,
    EmbeddingStatus,
    ParseStatus,
)
from app.repositories.document_repository import DocumentRepository


class DocumentWorkflowService:
    """
    Manages the processing lifecycle of a document.
    """

    def __init__(
        self,
        document_repository: DocumentRepository,
    ) -> None:
        self.document_repository = document_repository

    async def get_pending(
        self,
        limit: int,
    ) -> list[Document]:
        return await self.document_repository.get_pending_for_processing(limit)

    async def get_pending_for_embedding(
        self,
        limit: int,
    ) -> list[Document]:
        return await self.document_repository.get_pending_for_embedding(limit)

    async def get_document(
        self,
        document_id: UUID,
    ) -> Document | None:
        return await self.document_repository.get_by_id(document_id)

    async def get_pending_for_chunking(
        self,
        limit: int,
    ) -> list[Document]:
        return await self.document_repository.get_pending_for_chunking(limit=limit)

    async def begin_processing(
        self,
        document_id: UUID,
    ) -> Document | None:
        document = await self.get_document(document_id)

        if document is None:
            return None

        document.document_status = DocumentStatus.PROCESSING
        document.parse_status = ParseStatus.RUNNING

        return await self.document_repository.update(document)

    async def mark_parsing_completed(
        self,
        document: Document,
    ) -> Document:
        document.parse_status = ParseStatus.COMPLETED
        document.chunk_status = ChunkStatus.PENDING

        return await self.document_repository.update(document)

    async def mark_parsing_failed(
        self,
        document: Document,
    ) -> Document:
        document.document_status = DocumentStatus.FAILED
        document.parse_status = ParseStatus.FAILED

        return await self.document_repository.update(document)

    async def begin_chunking(
        self,
        document: Document,
    ) -> Document:
        document.chunk_status = ChunkStatus.RUNNING

        return await self.document_repository.update(document)

    async def mark_chunking_completed(
        self,
        document: Document,
    ) -> Document:
        document.chunk_status = ChunkStatus.COMPLETED
        document.embedding_status = EmbeddingStatus.PENDING

        return await self.document_repository.update(document)

    async def mark_chunking_failed(
        self,
        document: Document,
    ) -> Document:
        document.chunk_status = ChunkStatus.FAILED
        document.document_status = DocumentStatus.FAILED

        return await self.document_repository.update(document)

    async def begin_embedding(
        self,
        document: Document,
    ) -> Document:
        document.embedding_status = EmbeddingStatus.RUNNING

        return await self.document_repository.update(document)

    async def mark_embedding_completed(
        self,
        document: Document,
    ) -> Document:
        document.embedding_status = EmbeddingStatus.COMPLETED
        document.document_status = DocumentStatus.READY

        return await self.document_repository.update(document)

    async def mark_embedding_failed(
        self,
        document: Document,
    ) -> Document:
        document.embedding_status = EmbeddingStatus.FAILED
        document.document_status = DocumentStatus.FAILED

        return await self.document_repository.update(document)