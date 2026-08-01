from http import HTTPStatus
from app.core.exceptions.base import AppException
from app.core.exceptions.internal import InternalServerException

def test_internal_exception_instance_type():
    """Verify that InternalServerException inherits from AppException."""
    # Arrange & Act
    exc = InternalServerException(
        detail="Internal server error."
    )

    # Assert
    assert isinstance(exc, AppException)

def test_internal_exception_stores_default_status_code():
    """Verify that InternalServerException uses HTTP 500 by default."""
    # Arrange & Act
    exc = InternalServerException(
        detail="Internal server error"
    )

    # Assert
    assert exc.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

def test_internal_exception_to_dict_returns_expected_values():
    """Verify that InternalServerException serializes its properties correctly."""
    # Arrange & Act
    expected_detail = "Internal server error"
    expected_extra = {"ip": "127.0.0.1"}
    exc = InternalServerException(
        detail=expected_detail,
        extra=expected_extra
    )

    # Act
    result_dict = exc.to_dict()

    # Assert
    assert result_dict["error"] == "INTERNAL_ERROR"
    assert result_dict["detail"] == expected_detail
    assert result_dict["status_code"] == HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert result_dict["extra"] == expected_extra