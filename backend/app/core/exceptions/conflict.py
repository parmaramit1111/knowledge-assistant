from typing import Optional, Any
from http import HTTPStatus
from .base import AppException
from app.schemas.api_response import ResponseCode

class ConflictException(AppException):
    """Exception raised when there is a conflict."""

    STATUS: HTTPStatus = HTTPStatus.CONFLICT

    def __init__(self, detail: str = "Conflict", *, extra: Optional[dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=self.STATUS,
            detail=detail,
            code=ResponseCode.CONFLICT,
            extra=extra
        )
