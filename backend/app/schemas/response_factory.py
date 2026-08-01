from typing import TypeVar
from app.schemas.api_response import ApiResponse, ResponseCode
from app.core.middleware.request_context import get_request_id


T = TypeVar("T")

class ResponseFactory:

    @staticmethod
    def success(
        result: T,
        message: str = "Success",
    ) -> ApiResponse[T]:

        return ApiResponse[T](
            code=ResponseCode.SUCCESS,
            success=True,
            message=message,
            result=result,
            request_id=get_request_id()
        )

    @staticmethod
    def error(
        code: ResponseCode,
        message: str
    ) -> ApiResponse:
        return ApiResponse(
            code=code,
            success=False,
            message=message,
            request_id=get_request_id()
        )

    @staticmethod
    def validation_error(message:str ="Validation error"):
        return ApiResponse(
            code=ResponseCode.VALIDATION_ERROR,
            success=False,
            message=message,
            request_id=get_request_id()
        )

    @staticmethod
    def not_found(message="Resource not found"):
        return ApiResponse(
            code=ResponseCode.NOT_FOUND,
            success=False,
            message=message,
            request_id=get_request_id()
        )

    @staticmethod
    def unauthorized(message="Unauthorized"):
        return ApiResponse(
            code=ResponseCode.UNAUTHORIZED,
            success=False,
            message=message,
            request_id=get_request_id()
        )

    @staticmethod
    def internal_error():
        return ApiResponse(
            code=ResponseCode.INTERNAL_SERVER_ERROR,
            success=False,
            message="An unexpected error occurred",
            request_id=get_request_id()
        )