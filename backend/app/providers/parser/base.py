from abc import ABC, abstractmethod
from pathlib import Path

from app.models.document import Document
from app.models.parsed_document import ParsedDocument


class BaseParser(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Parser name."""

    @property
    @abstractmethod
    def version(self) -> str:
        """Parser version."""

    @property
    @abstractmethod
    def supported_content_types(self) -> list[str]:
        """Supported MIME types."""

    @abstractmethod
    async def parse(
        self,
        document: Document,
    ) -> ParsedDocument:
        """Parse a document into a ParsedDocument."""

    def _get_document_path(
        self,
        document: Document,
    ) -> Path:
        """Get the path to the document file."""
        if not document.storage_path:
            raise ValueError(
                "Document has no storage path."
            )

        path = Path(document.storage_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document file not found: {path}"
            )
        return path