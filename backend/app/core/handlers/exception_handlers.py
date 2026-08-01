from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.schemas.response_factory import ResponseFactory
from app.core.exceptions.base import AppException

def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all exception handlers for the FastAPI application.
    """

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        """
        Handle custom AppException and return a JSON response.

        Args:
            request (Request): The incoming request.
            exc (AppException): The caught AppException.

        Returns:
            JSONResponse: A JSON response with the error details.
        """
        response = ResponseFactory.error(
            code=exc.code,
            message=exc.detail,
        )

        return JSONResponse(
            status_code=exc.status_code.value,
            content=response.model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Handle unexpected exceptions and return a generic error response.

        Args:
            request (Request): The incoming request.
            exc (Exception): The caught unexpected exception.

        Returns:
            JSONResponse: A JSON response with a generic error message.
        """

        # TODO: Log unexpected exceptions with stack trace.
        response = ResponseFactory.internal_error()

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            content=response.model_dump(),
        )