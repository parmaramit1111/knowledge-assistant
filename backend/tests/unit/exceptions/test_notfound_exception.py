from http import HTTPStatus
from app.exceptions.base import AppException
from app.exceptions.not_found import ResourceNotFoundException

def test_not_found_exception_instance_type():
    """Verify that ResourceNotFoundException inherits from AppException."""
    # Arrange & Act
    expected_detail = "Resource not found Exception"
    exc = ResourceNotFoundException(
        detail=expected_detail
    )

    # Assert
    assert isinstance(exc, AppException)

def test_not_found_exception_stores_default_status_code():
    """Verify that ResourceNotFoundException uses HTTP 404 by default."""
    # Arrange & Act
    exc = ResourceNotFoundException(
        detail="Forbidden"
    )

    # Assert
    assert exc.status_code == HTTPStatus.NOT_FOUND

def test_not_found_exception_to_dict_returns_expected_values():
    """Verify that ResourceNotFoundException serializes its properties correctly."""
    # Arrange & Act
    expected_detail = "Resource not found Exception"
    expected_extra = {"ip": "127.0.0.1"}
    exc = ResourceNotFoundException(
        detail=expected_detail,
        extra=expected_extra
    )

    # Act
    result_dict = exc.to_dict()

    # Assert
    assert result_dict["error"] == "NOT_FOUND"
    assert result_dict["detail"] == expected_detail
    assert result_dict["status_code"] == HTTPStatus.NOT_FOUND.value
    assert result_dict["extra"] == expected_extra