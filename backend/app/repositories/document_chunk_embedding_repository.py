from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.dtos.search_result import SearchResult
from app.models.document import Document
from app.models.document_chunk_embedding import DocumentChunkEmbedding
from app.models.document_chunk import DocumentChunk
from .base import BaseRepository


class DocumentChunkEmbeddingRepository(BaseRepository[DocumentChunkEmbedding]):
    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(
            session,
            DocumentChunkEmbedding,
        )

    async def get(self, id: UUID,) -> DocumentChunkEmbedding | None:
        return await self.get_by_id(id)

    async def similarity_search(
        self,
        query_embedding:list[float],
        top_k:int
    ) -> list[SearchResult]:
        distance_expr = DocumentChunkEmbedding.embedding.cosine_distance(query_embedding)
        similarity_expr = (1 - distance_expr)
        similarity_score = similarity_expr.label("similarity_score")

        statement = (
            select(
                DocumentChunk.id,
                DocumentChunk.document_id,
                Document.original_filename,
                DocumentChunk.content,
                DocumentChunk.chunk_index,
                similarity_score,
            )
            .join(
                DocumentChunk,
                DocumentChunk.id == DocumentChunkEmbedding.document_chunk_id
            )
            .join(
                Document,
                Document.id == DocumentChunk.document_id
            )
            .where((1 - distance_expr) >= settings.search_similarity_threshold)
            .order_by(distance_expr)
            .limit(top_k)
        )
        result = await self._session.execute(statement)

        rows = result.all()

        return [
            SearchResult(
                chunk_id=row.id,
                document_id=row.document_id,
                document_name=row.original_filename,
                content=row.content,
                chunk_index=row.chunk_index,
                similarity_score=row.similarity_score,
            )
            for row in rows
        ]
