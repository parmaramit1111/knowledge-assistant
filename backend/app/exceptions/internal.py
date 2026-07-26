from typing import Optional, Any
from http import HTTPStatus
from .base import AppException

class InternalServerException(AppException):
    """Exception raised when there is an internal server error."""

    STATUS: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
    CODE: str = "INTERNAL_ERROR"

    def __init__(self, detail: str = "Internal server error", *, extra: Optional[dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=self.STATUS,
            detail=detail,
            code=self.CODE,
            extra=extra
        )
