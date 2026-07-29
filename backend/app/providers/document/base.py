"""
Base interface for document parsers.

Every document parser must implement this interface and return a
ParsedDocument irrespective of the underlying file format.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from app.models.document import ParsedDocument


class BaseDocumentParser(ABC):
    """Abstract base class for all document parsers."""

    @abstractmethod
    def parse(self, file_path: Path) -> ParsedDocument:
        """
        Parse a document and return its structured representation.

        Args:
            file_path: Path to the document.

        Returns:
            ParsedDocument containing extracted content and metadata.

        Raises:
            DocumentParsingError:
                If the document cannot be parsed.
        """
        raise NotImplementedError