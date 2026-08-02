from dataclasses import dataclass
from uuid import UUID

from app.commands import Command
from app.core.execution.context import ExecutionContext
from app.core.execution.transactional import transactional

@dataclass(slots=True)
class ParseDocumentCommand(Command[None]):
    context: ExecutionContext
    document_id: UUID

    @transactional
    async def execute(
        self,
    ) -> None:
        await self.context.document_processing_service.process_document(
            self.document_id,
        )
