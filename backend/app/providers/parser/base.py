from abc import ABC, abstractmethod

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