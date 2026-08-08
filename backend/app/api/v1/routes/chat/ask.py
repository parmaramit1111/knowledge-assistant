from fastapi import APIRouter, status

from app.core.execution.context import ExecutionContext
from app.commands.chat.ask_question_command import AskQuestionCommand
from app.schemas.api_response import ApiResponse
from app.schemas.chat_request import ChatRequest
from app.schemas.chat_response import ChatResponse
from app.schemas.response_factory import ResponseFactory

from .docs import (
    CHAT_DESCRIPTION,
    CHAT_SUCCESS_DESCRIPTION,
    CHAT_SUMMARY,
)

router = APIRouter()


@router.post(
    "/",
    response_model=ApiResponse[ChatResponse],
    status_code=status.HTTP_200_OK,
    summary=CHAT_SUMMARY,
    description=CHAT_DESCRIPTION,
    responses={
        status.HTTP_200_OK: {
            "description": CHAT_SUCCESS_DESCRIPTION,
        }
    },
)
async def ask_question(
    chat_request: ChatRequest,
) -> ApiResponse[ChatResponse]:

    async with ExecutionContext() as context:
        command = AskQuestionCommand(context)

        chat_result = await command.execute(
            chat_request,
        )

        return ResponseFactory.success(
            result=ChatResponse.model_validate(chat_result),
            message="Question answered successfully.",
        )