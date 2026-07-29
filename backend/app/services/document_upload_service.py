from pathlib import Path
from uuid import uuid4

from app.commands.upload.upload_document import UploadDocumentCommand
from app.core.config import settings
from app.models.document import Document


class DocumentUploadService:
    async def execute(self, command: UploadDocumentCommand) -> Document:
        file = command.file

        # Validation
        if file.content_type not in settings.allowed_content_types:
            raise ValueError("Unsupported file type.")

        contents = await file.read()

        if not contents:
            raise ValueError("Uploaded file is empty.")

        if len(contents) > settings.max_upload_size:
            raise ValueError("File size exceeds the allowed limit.")

        # Generate identifiers
        document_id = uuid4()
        filename = f"{document_id}.pdf"

        # Storage
        upload_directory = Path(settings.upload_directory)
        upload_directory.mkdir(parents=True, exist_ok=True)

        storage_path = upload_directory / filename

        storage_path.write_bytes(contents)

        # Domain Model
        return Document(
            id=document_id,
            filename=filename,
            original_filename=file.filename or filename,
            content_type=file.content_type,
            size=len(contents),
            storage_path=storage_path,
        )