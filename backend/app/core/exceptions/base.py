from typing import Any, Optional
from http import HTTPStatus
from app.schemas.api_response import ResponseCode

class AppException(Exception):
    """Base exception for the entire application."""

    def __init__(
        self,
        status_code: HTTPStatus,
        detail: str,
        *,
        code: ResponseCode,
        extra: Optional[dict[str, Any]] = None,
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        self.code = code
        self.extra = extra or {}
        super().__init__(detail)

    def to_dict(self) -> dict[str, Any]:
        """Common serialization method — every handler can use this."""
        payload = {
            "error": self.code,
            "detail": self.detail,
            "status_code": self.status_code.value,
        }
        if self.extra:
            payload["extra"] = self.extra
        return payload

class StorageException(AppException):
    """Exceptions related to storage operations."""

    STATUS: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, detail: str = "Storage operation failed", *, extra: Optional[dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=self.STATUS,
            detail=detail,
            code=ResponseCode.INTERNAL_SERVER_ERROR,
            extra=extra
        )

class CustomException(AppException):
    """Custom exceptions."""
    def __init__(self, status_code: HTTPStatus, detail: str, code: ResponseCode, *, extra: Optional[dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail,
            code=code,
            extra=extra
        )