from app.core.execution.context import ExecutionContext
from app.commands.document.parse_document_command import ParseDocumentCommand
from app.core.config import settings
from app.workers.base import BaseWorker

class DocumentWorker(BaseWorker):
    """
    Background worker responsible for processing uploaded documents.
    """

    async def run(self) -> None:
        async with ExecutionContext() as context:
            documents = await context.document_processing_service.get_pending(limit=settings.worker_batch_size)

            if not documents:
                return

            for document in documents:
                async with ExecutionContext() as current_context:
                    command = ParseDocumentCommand(
                        context=current_context,
                        document_id=document.id,
                    )

                    await command.execute()