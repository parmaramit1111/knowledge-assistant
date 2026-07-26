from typing import Optional, Any
from http import HTTPStatus
from .base import AppException

class ConflictException(AppException):
    """Exception raised when there is a conflict."""

    STATUS: HTTPStatus = HTTPStatus.CONFLICT
    CODE: str = "CONFLICT"

    def __init__(self, detail: str = "Conflict", *, extra: Optional[dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=self.STATUS,
            detail=detail,
            code=self.CODE,
            extra=extra
        )
