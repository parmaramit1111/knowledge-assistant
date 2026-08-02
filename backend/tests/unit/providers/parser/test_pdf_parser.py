
import pytest
from pathlib import Path
from uuid import uuid4

from app.models.document import Document
from app.providers.parser.pdf_parser import PdfParser

FIXTURE_DIR = Path(__file__).resolve().parents[2] / "fixtures"

@pytest.mark.asyncio
async def test_parse_valid_pdf():

    document = Document(
        id=uuid4(),
        storage_path=str(FIXTURE_DIR / "sample.pdf"),
        content_type="application/pdf",
    )

    parser = PdfParser()

    parsed = await parser.parse(document)

    assert parsed.document_id == document.id
    assert parsed.content != ""
    assert parsed.parser_name == "PyMuPDF"
    assert parsed.parser_version
    assert parsed.parser_metadata is not None
    assert parsed.parser_metadata["page_count"] > 0 # type: ignore

@pytest.mark.asyncio
async def test_parse_without_storage_path():

    document = Document(
        id=uuid4(),
        storage_path="",
        content_type="application/pdf",
    )

    parser = PdfParser()

    with pytest.raises(ValueError):
        await parser.parse(document)

@pytest.mark.asyncio
async def test_parse_missing_file():

    document = Document(
        id=uuid4(),
        storage_path=str(FIXTURE_DIR / "not_found.pdf"),
        content_type="application/pdf",
    )

    parser = PdfParser()

    with pytest.raises(FileNotFoundError):
        await parser.parse(document)