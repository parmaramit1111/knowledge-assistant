from dataclasses import dataclass
from uuid import UUID

from app.commands import Command
from app.core.execution.context import ExecutionContext
from app.core.execution.transactional import transactional

@dataclass(slots=True)
class EmbedDocumentCommand(Command[None]):
    context: ExecutionContext
    document_id: UUID

    @transactional
    async def execute(
        self,
    ) -> None:
        await self.context.document_embedding_service.embed_document(
            document_id=self.document_id,
        )
