from http import HTTPStatus
from app.core.exceptions.base import AppException
from app.core.exceptions.authorization import UnauthorizedException

def test_authorization_exception_instance_type():
    """Verify that UnauthorizedException inherits from AppException."""
    # Arrange & Act
    exc = UnauthorizedException(
        detail="Unauthorized Access."
    )

    # Assert
    assert isinstance(exc, AppException)

def test_authorization_exception_stores_default_status_code():
    """Verify that UnauthorizedException uses HTTP 401 by default."""
    # Arrange & Act
    exc = UnauthorizedException(
        detail="Unauthorized Access"
    )

    # Assert
    assert exc.status_code == HTTPStatus.UNAUTHORIZED

def test_authorization_exception_to_dict_returns_expected_values():
    """Verify that UnauthorizedException serializes its properties correctly."""
    # Arrange & Act
    expected_detail = "Unauthorized Access"
    expected_extra = {"ip": "127.0.0.1"}
    exc = UnauthorizedException(
        detail=expected_detail,
        extra=expected_extra
    )

    # Act
    result_dict = exc.to_dict()

    # Assert
    assert result_dict["error"] == "UNAUTHORIZED"
    assert result_dict["detail"] == expected_detail
    assert result_dict["status_code"] == HTTPStatus.UNAUTHORIZED.value
    assert result_dict["extra"] == expected_extra