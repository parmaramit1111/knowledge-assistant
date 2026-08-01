from dataclasses import dataclass
from uuid import UUID

from app.commands import Command
from app.core.transaction.transactional import transactional
from app.core.dependencies.service_factory import ServiceFactory

@dataclass(slots=True)
class ParseDocumentCommand(Command[None]):

    document_id: UUID

    @transactional
    async def execute(self):
        document_processing_service = ServiceFactory.document_processing_service()

        await document_processing_service.process_document(self.document_id)

