from bs4 import BeautifulSoup

from app.models.document import Document
from app.models.parsed_document import ParsedDocument

from app.providers.parser.base import BaseParser


class HtmlParser(BaseParser):

    @property
    def name(self) -> str:
        return "BeautifulSoup"

    @property
    def version(self) -> str:
        return "1.0"

    @property
    def supported_content_types(self) -> list[str]:
        return [
            "text/html",
            "application/xhtml+xml",
        ]

    async def parse(
        self,
        document: Document,
    ) -> ParsedDocument:
        path = self._get_document_path(document)

        html = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        content = soup.get_text(
            separator="\n",
            strip=True,
        )

        parser_metadata = {
            "title": soup.title.string.strip()
                if soup.title and soup.title.string
                else "",
            "language": "",
            "character_count": len(content),
        }

        return ParsedDocument(
            document_id=document.id,
            content=content,
            parser_name=self.name,
            parser_version=self.version,
            parser_metadata=parser_metadata,
        )