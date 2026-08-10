
import pytest
from pathlib import Path
from uuid import uuid4

from app.models.document import Document
from app.providers.parser.word_parser import WordParser

FIXTURE_DIR = Path(__file__).resolve().parents[2] / "fixtures"

@pytest.mark.asyncio
async def test_parse_valid_text():

    document = Document(
        id=uuid4(),
        storage_path=str(FIXTURE_DIR / "sample.docx"),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    parser = WordParser()

    parsed = await parser.parse(document)

    assert parsed.document_id == document.id
    assert parsed.content != ""
    assert parsed.parser_name == "PythonDocx"
    assert parsed.parser_version
    assert parsed.parser_metadata is not None
    assert parsed.parser_metadata["paragraph_count"] >= 0 # type: ignore
    assert parsed.parser_metadata["section_count"] >= 0 # type: ignore
    assert parsed.parser_metadata["table_count"] >= 0 # type: ignore

@pytest.mark.asyncio
async def test_parse_without_storage_path():

    document = Document(
        id=uuid4(),
        storage_path="",
        content_type="text/plain",
    )

    parser = WordParser()

    with pytest.raises(ValueError):
        await parser.parse(document)

@pytest.mark.asyncio
async def test_parse_missing_file():

    document = Document(
        id=uuid4(),
        storage_path=str(FIXTURE_DIR / "not_found.docx"),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    parser = WordParser()

    with pytest.raises(FileNotFoundError):
        await parser.parse(document)