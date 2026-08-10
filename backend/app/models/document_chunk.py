from uuid import UUID

from sqlalchemy import (
    String,
    ForeignKey,
    Integer,
    Text,
    JSON,
    UniqueConstraint
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import BaseEntity
from app.models.document import EmbeddingStatus


class DocumentChunk(BaseEntity):
    """
    Represents a semantic chunk extracted from a parsed document.
    """
    __tablename__ = "document_chunks"

    __table_args__ = (
        UniqueConstraint(
            "parsed_document_id",
            "chunk_index",
            name="uq_document_chunk_index",
        ),
    )

    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
        index=True,
    )

    parsed_document_id: Mapped[UUID] = mapped_column(
        ForeignKey("parsed_documents.id"),
        nullable=False,
        index=True,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    chunker_name: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
    )
    chunker_version: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    character_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    token_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    chunk_metadata: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    embedding_status: Mapped[EmbeddingStatus] = mapped_column(
        nullable=False,
        default=EmbeddingStatus.PENDING,
        index=True,
    )