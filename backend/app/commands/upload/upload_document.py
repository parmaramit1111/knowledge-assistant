from dataclasses import dataclass

from fastapi import UploadFile

from app.commands import Command
from app.core.dependencies.service_factory import ServiceFactory
from app.core.transaction.transactional import transactional
from app.schemas.document import UploadResponse


@dataclass(slots=True)
class UploadDocumentCommand(Command[UploadResponse]):
    """
    Upload a document.
    """

    file: UploadFile

    @transactional
    async def execute(self) -> UploadResponse:
        service = ServiceFactory.document_service()

        return await service.upload(
            file=self.file,
        )