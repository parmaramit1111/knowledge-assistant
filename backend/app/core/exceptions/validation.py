from typing import Optional, Any
from http import HTTPStatus
from .base import AppException
from app.schemas.api_response import ResponseCode

class ValidationException(AppException):
    """Exception raised when there is a validation error."""

    STATUS: HTTPStatus = HTTPStatus.UNPROCESSABLE_ENTITY

    def __init__(self, detail: str = "Validation error", *, extra: Optional[dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=self.STATUS,
            detail=detail,
            code=ResponseCode.VALIDATION_ERROR,
            extra=extra
        )
