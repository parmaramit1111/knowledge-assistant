import pytest
from http import HTTPStatus
from app.core.exceptions.base import AppException

def test_app_exception_stores_status_code():
    """Verify that the exception correctly stores the HTTP status code."""
    # Arrange & Act
    exc = AppException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail="Invalid input",
        code="INVALID_INPUT"
    )

    # Assert
    assert exc.status_code == HTTPStatus.BAD_REQUEST


def test_app_exception_stores_detail():
    """Verify that the exception correctly stores the detail message."""
    # Arrange & Act
    expected_detail = "Resource not found"
    exc = AppException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=expected_detail,
        code="NOT_FOUND"
    )

    # Assert
    assert exc.detail == expected_detail
    assert str(exc) == expected_detail  # Verifies super().__init__(detail) worked


def test_app_exception_to_dict_returns_expected_structure():
    """Verify that to_dict() serializes all fields properly, including extra payload."""
    # Arrange
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    detail = "Database connection failed"
    code = "DB_ERROR"
    extra_data = {"database": "users_db", "retry": True}

    exc = AppException(
        status_code=status,
        detail=detail,
        code=code,
        extra=extra_data
    )

    # Act
    result_dict = exc.to_dict()

    # Assert
    expected_dict = {
        "error": "DB_ERROR",
        "detail": "Database connection failed",
        "status_code": 500,
        "extra": {"database": "users_db", "retry": True}
    }
    assert result_dict == expected_dict
