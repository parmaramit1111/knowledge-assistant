from http import HTTPStatus
from app.core.exceptions.base import AppException
from app.core.exceptions.validation import ValidationException

def test_validation_exception_instance_type():
    """Verify that ValidationException inherits from AppException."""
    # Arrange & Act
    exc = ValidationException(
        detail="User name is required."
    )

    # Assert
    assert isinstance(exc, AppException)

def test_validation_exception_stores_default_status_code():
    """Verify that ValidationException uses HTTP 422 by default."""
    # Arrange & Act
    exc = ValidationException(
        detail="User name is required."
    )

    # Assert
    assert exc.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

def test_validation_exception_to_dict_returns_expected_values():
    """Verify that ValidationException serializes its properties correctly."""
    # Arrange & Act
    expected_detail = "User name is required."
    expected_extra = {"user_name": "User name is required."}
    exc = ValidationException(
        detail=expected_detail,
        extra=expected_extra
    )

    # Act
    result_dict = exc.to_dict()

    # Assert
    assert result_dict["error"] == "VALIDATION_ERROR"
    assert result_dict["detail"] == expected_detail
    assert result_dict["status_code"] == HTTPStatus.UNPROCESSABLE_ENTITY.value
    assert result_dict["extra"] == expected_extra