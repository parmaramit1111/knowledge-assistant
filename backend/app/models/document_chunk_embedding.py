from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    JSON,
)
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import BaseEntity


class DocumentChunkEmbedding(BaseEntity):
    """
    Stores the vector embedding generated for a document chunk.
    """

    __tablename__ = "document_chunk_embeddings"

    document_chunk_id: Mapped[UUID] = mapped_column(
        ForeignKey("document_chunks.id"),
        nullable=False,
        index=True,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    provider_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    provider_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    dimensions: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(384),
        nullable=False,
    )

    embedding_metadata: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )