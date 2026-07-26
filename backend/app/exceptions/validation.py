from typing import Optional, Any
from http import HTTPStatus
from .base import AppException

class ValidationException(AppException):
    """Exception raised when there is a validation error."""

    STATUS: HTTPStatus = HTTPStatus.UNPROCESSABLE_ENTITY
    CODE: str = "VALIDATION_ERROR"

    def __init__(self, detail: str = "Validation error", *, extra: Optional[dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=self.STATUS,
            detail=detail,
            code=self.CODE,
            extra=extra
        )
