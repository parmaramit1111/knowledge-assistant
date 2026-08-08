from dataclasses import dataclass

from app.commands import Command
from app.core.execution.context import ExecutionContext

from app.schemas.chat_request import ChatRequest
from app.schemas.chat_response import ChatResponse

@dataclass(slots=True)
class AskQuestionCommand(Command[ChatResponse]):
    context: ExecutionContext

    async def execute(
        self,
        chat_request: ChatRequest
    ) -> ChatResponse:

        return await self.context.document_chat_service.ask(chat_request)
