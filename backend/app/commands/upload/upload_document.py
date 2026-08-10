from dataclasses import dataclass

from fastapi import UploadFile

from app.commands import Command
from app.core.execution.context import ExecutionContext
from app.core.execution.transactional import transactional
from app.schemas.document import UploadResponse
from app.core.exceptions.validation import UnsupportedDocumentTypeError

SUPPORTED_CONTENT_TYPES = {
    "application/pdf",
    "text/plain",
    "text/markdown",
    "text/x-markdown",
    "text/html",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

@dataclass(slots=True)
class UploadDocumentCommand(Command[UploadResponse]):
    """
    Upload a document.
    """
    context: ExecutionContext

    file: UploadFile

    @transactional
    async def execute(self) -> UploadResponse:
        """
        Execute the command.
        """
        if self.file.content_type not in SUPPORTED_CONTENT_TYPES:
            raise UnsupportedDocumentTypeError(str(self.file.content_type))

        return await self.context.document_upload_service.upload(
            file=self.file,
        )