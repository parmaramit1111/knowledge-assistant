from app.models.document import Document
from app.models.parsed_document import ParsedDocument

from app.providers.parser.base import BaseParser


class MarkdownParser(BaseParser):

    @property
    def name(self) -> str:
        return "MarkdownParser"

    @property
    def version(self) -> str:
        return "1.0"

    @property
    def supported_content_types(self) -> list[str]:
        return [
            "text/markdown",
            "text/x-markdown",
        ]

    async def parse(
        self,
        document: Document,
    ) -> ParsedDocument:
        path = self._get_document_path(
            document
        )

        content = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        parser_metadata = {
            "line_count": len(content.splitlines()),
            "character_count": len(content),
            "language": "",
        }

        return ParsedDocument(
            document_id=document.id,
            content=content,
            parser_name=self.name,
            parser_version=self.version,
            parser_metadata=parser_metadata,
        )