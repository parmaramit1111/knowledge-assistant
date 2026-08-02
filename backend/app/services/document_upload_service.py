from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions.base import StorageException
from app.core.exceptions.validation import ValidationException
from app.models.document import (
    Document,
    DocumentStatus,
    ParseStatus,
    EmbeddingStatus,
)
from app.schemas.document import UploadResponse
from app.repositories.document_repository import DocumentRepository

class DocumentUploadService:
    """
    Handles document upload business logic.
    """

    def __init__(
        self,
        document_repository: DocumentRepository,
    ) -> None:
        self.document_repository =  document_repository

    async def upload(
        self,
        file: UploadFile,
    ) -> UploadResponse:

        content_type = file.content_type or ""

        if content_type not in settings.allowed_content_types:
            raise ValidationException("Unsupported file type.")

        contents = await file.read()

        if not contents:
            raise ValidationException("Uploaded file is empty.")

        if len(contents) > settings.max_upload_size:
            raise ValidationException("File size exceeds the allowed limit.")

        extension = Path(file.filename or "").suffix.lower()

        if not extension:
            raise ValidationException("File extension is missing.")

        filename = f"{uuid4()}{extension}"

        upload_directory = Path(settings.upload_directory)
        upload_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        storage_path = upload_directory / filename

        try:
            storage_path.write_bytes(contents)

        except OSError as ex:
            raise StorageException() from ex

        document = Document(
            filename=filename,
            original_filename=file.filename or filename,
            content_type=content_type,
            size=len(contents),
            storage_path=str(storage_path),
            document_status=DocumentStatus.UPLOADED,
            parse_status=ParseStatus.PENDING,
            embedding_status=EmbeddingStatus.PENDING,
        )

        document = await self.document_repository.add(document)

        return UploadResponse.model_validate(document)