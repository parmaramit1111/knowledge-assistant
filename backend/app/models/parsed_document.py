from uuid import UUID
from sqlalchemy import String, JSON, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.document import Document

class ParsedDocument(BaseEntity):
    """Parsed Document model."""
    __tablename__ = "parsed_documents"

    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("documents.id"),
        unique=True,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    parser_name: Mapped[str] = mapped_column(
        String(30),
        nullable=True,
    )

    parser_version: Mapped[str] = mapped_column(
        String(5),
        nullable=True,
    )

    parser_metadata: Mapped[JSON] = mapped_column(
        JSON,
        nullable=True,
    )

    # Optional: Python-side relationship definition
    document: Mapped["Document"] = relationship(
        back_populates="parsed_document",
    )
