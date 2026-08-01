from http import HTTPStatus
from app.core.exceptions.base import AppException
from app.core.exceptions.authorization import ForbiddenException

def test_forbidden_exception_instance_type():
    """Verify that ForbiddenException inherits from AppException."""
    # Arrange & Act
    exc = ForbiddenException(
        detail="Forbidden."
    )

    # Assert
    assert isinstance(exc, AppException)

def test_forbidden_exception_stores_default_status_code():
    """Verify that ForbiddenException uses HTTP 403 by default."""
    # Arrange & Act
    exc = ForbiddenException(
        detail="Forbidden"
    )

    # Assert
    assert exc.status_code == HTTPStatus.FORBIDDEN

def test_forbidden_exception_to_dict_returns_expected_values():
    """Verify that ForbiddenException serializes its properties correctly."""
    # Arrange & Act
    expected_detail = "Forbidden"
    expected_extra = {"ip": "127.0.0.1"}
    exc = ForbiddenException(
        detail=expected_detail,
        extra=expected_extra
    )

    # Act
    result_dict = exc.to_dict()

    # Assert
    assert result_dict["error"] == "FORBIDDEN"
    assert result_dict["detail"] == expected_detail
    assert result_dict["status_code"] == HTTPStatus.FORBIDDEN.value
    assert result_dict["extra"] == expected_extra