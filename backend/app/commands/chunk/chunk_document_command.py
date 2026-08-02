from dataclasses import dataclass
from uuid import UUID

from app.commands import Command
from app.core.execution.context import ExecutionContext
from app.core.execution.transactional import transactional

@dataclass(slots=True)
class ChunkDocumentCommand(Command[None]):
    context: ExecutionContext
    document_id: UUID

    @transactional
    async def execute(
        self,
    ) -> None:
        await self.context.document_chunking_service.chunk_document(
            self.document_id,
        )
