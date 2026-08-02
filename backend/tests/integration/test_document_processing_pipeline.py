from pathlib import Path
from uuid import uuid4

import pytest

from app.models.document import (
    Document,
    DocumentStatus,
    ParseStatus,
)
from app.providers.parser.pdf_parser import PdfParser


@pytest.mark.asyncio
async def test_document_processing_pipeline():

    #
    # Arrange
    #

    fixture = (
        Path(__file__).resolve().parents[1]
        / "unit"
        / "fixtures"
        / "sample.pdf"
    )

    document = Document(
        id=uuid4(),
        filename="sample.pdf",
        original_filename="sample.pdf",
        content_type="application/pdf",
        size=fixture.stat().st_size,
        storage_path=str(fixture),
        document_status=DocumentStatus.UPLOADED,
        parse_status=ParseStatus.PENDING,
    )

    #
    # Act
    #

    parser = PdfParser()

    parsed = await parser.parse(document)

    #
    # Assert
    #

    assert parsed is not None
    assert parsed.document_id == document.id
    assert parsed.content != ""
    assert parsed.parser_name == "PyMuPDF"
    assert parsed.parser_version
    assert parsed.parser_metadata is not None
    assert parsed.parser_metadata["page_count"] > 0 # type: ignore #