from enum import Enum
from sqlalchemy import String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.parsed_document import ParsedDocument

class DocumentStatus(str, Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"

class ParseStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class EmbeddingStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ChunkStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Document(BaseEntity):
    """Document model."""
    __tablename__ = "documents"

    filename: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )
    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    size: Mapped[int] = mapped_column(
        nullable=False,
    )

    storage_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    document_status: Mapped[DocumentStatus] = mapped_column(
        SqlEnum(
            DocumentStatus,
            name="document_status",
        ),
        nullable=False,
        default=DocumentStatus.UPLOADED,
    )
    parse_status: Mapped[ParseStatus] = mapped_column(
        SqlEnum(
            ParseStatus,
            name="parse_status",
        ),
        nullable=False,
        default=ParseStatus.PENDING,
    )
    embedding_status: Mapped[EmbeddingStatus] = mapped_column(
        SqlEnum(
            EmbeddingStatus,
            name="embedding_status",
        ),
        nullable=False,
        default=EmbeddingStatus.PENDING,
    )
    chunk_status: Mapped[ChunkStatus] = mapped_column(
        SqlEnum(
            ChunkStatus,
            name="chunk_status",
        ),
        nullable=False,
        default=ChunkStatus.PENDING,
    )

    # Optional: Python-side relationship definition
    parsed_document: Mapped["ParsedDocument"] = relationship(
        back_populates="document",
    )