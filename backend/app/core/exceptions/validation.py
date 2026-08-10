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


class UnsupportedDocumentTypeError(AppException):
    """Exception raised when an unsupported document type is encountered."""

    STATUS: HTTPStatus = HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    def __init__(self, content_type: str, *, extra: Optional[dict[str, Any]] = None) -> None:
        detail = f"Unsupported document type: {content_type}"

        super().__init__(
            status_code=self.STATUS,
            detail=detail,
            code=ResponseCode.UNSUPPORTED_MEDIA_TYPE,
            extra=extra
        )