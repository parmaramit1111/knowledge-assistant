from http import HTTPStatus
from app.core.exceptions.base import AppException
from app.core.exceptions.conflict import ConflictException

def test_conflict_exception_instance_type():
    """Verify that ConflictException inherits from AppException."""
    # Arrange & Act
    expected_detail = "Resource already exists"
    exc = ConflictException(
        detail=expected_detail
    )

    # Assert
    assert isinstance(exc, AppException)

def test_conflict_exception_stores_default_status_code():
    """Verify that ConflictException uses HTTP 409 by default."""
    # Arrange & Act
    expected_detail = "Resource already exists"
    exc = ConflictException(
        detail=expected_detail
    )

    # Assert
    assert exc.status_code == HTTPStatus.CONFLICT

def test_conflict_exception_to_dict_returns_expected_values():
    """Verify that ConflictException serializes its properties correctly."""
    # Arrange & Act
    expected_detail = "Resource already exists"
    expected_extra = {"ip": "127.0.0.1"}
    exc = ConflictException(
        detail=expected_detail,
        extra=expected_extra
    )

    # Act
    result_dict = exc.to_dict()

    # Assert
    assert result_dict["error"] == "CONFLICT"
    assert result_dict["detail"] == expected_detail
    assert result_dict["status_code"] == HTTPStatus.CONFLICT.value
    assert result_dict["extra"] == expected_extra