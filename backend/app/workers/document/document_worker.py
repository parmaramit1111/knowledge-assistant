from app.commands.document.parse_document_command import ParseDocumentCommand
from app.core.dependencies.service_factory import ServiceFactory
from app.core.config import settings
from app.workers.base import BaseWorker

class DocumentWorker(BaseWorker):
    """
    Background worker responsible for processing uploaded documents.
    """

    async def run(self) -> None:

        service = ServiceFactory.document_processing_service()

        documents = await service.get_pending(limit=settings.worker_batch_size)

        if not documents:
            return

        for document in documents:
            command = ParseDocumentCommand(
                document_id=document.id,
            )

            await command.execute()