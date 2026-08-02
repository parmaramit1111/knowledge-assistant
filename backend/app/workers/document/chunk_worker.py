from app.core.logging import get_logger

from app.core.execution.context import ExecutionContext
from app.commands.chunk.chunk_document_command import ChunkDocumentCommand
from app.core.config import settings
from app.workers.base import BaseWorker

logger = get_logger(__name__)


class ChunkWorker(BaseWorker):
    """
    Background worker responsible for chunking documents.
    """

    async def run(self) -> None:
        async with ExecutionContext() as context:
            documents = await context.document_workflow_service.get_pending_for_chunking(
                limit=settings.worker_batch_size
            )

            if not documents:
                return

            for document in documents:
                async with ExecutionContext() as command_context:
                    try:
                        command = ChunkDocumentCommand(
                            context=command_context,
                            document_id=document.id,
                        )

                        await command.execute()

                    except Exception as e:
                        # Log the exception and potentially update the document status
                        logger.exception(
                            "Failed to chunk document %s",
                            document.id,
                        )

