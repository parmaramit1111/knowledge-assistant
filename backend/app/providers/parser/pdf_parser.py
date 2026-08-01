from pathlib import Path
import pymupdf

from app.providers.parser.base import BaseParser

from app.models.document import Document
from app.models.parsed_document import ParsedDocument

class PdfParser(BaseParser):

    @property
    def name(self) -> str:
        return "PyMuPDF"

    @property
    def version(self) -> str:
        return pymupdf.VersionBind

    @property
    def supported_content_types(self) -> list[str]:
        return [
            "application/pdf",
        ]

    async def parse(
        self,
        document: Document,
    ) -> ParsedDocument:
        if not document.storage_path:
            raise ValueError("Document has no storage path.")

        path = Path(document.storage_path)
        if not path.exists():
            raise FileNotFoundError(
                f"Document file not found: {path}"
            )

        with pymupdf.open(document.storage_path) as pdf:
            text = []
            for page in pdf:
                text.append(page.get_text().strip())

            content = "\n\n".join(text)

            metadata = pdf.metadata or {}
            parser_metadata = {
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "keywords": metadata.get("keywords", ""),
                "creator": metadata.get("creator", ""),
                "producer": metadata.get("producer", ""),
                "page_count": len(pdf),
                "language": "",
            }

            return ParsedDocument(
                document_id = document.id,
                content = content,
                parser_metadata = parser_metadata,
                parser_name = self.name,
                parser_version = self.version,
            )
