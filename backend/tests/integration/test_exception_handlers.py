from http import HTTPStatus
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.handlers.exception_handlers import register_exception_handlers
from app.exceptions.validation import ValidationException
from app.exceptions.not_found import ResourceNotFoundException
from app.exceptions.authorization import UnauthorizedException

# Update your test setup helper function:
def create_exception_test_client() -> TestClient:
    """Helper to configure an isolated app instance with your error handlers."""
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/error/validation")
    def trigger_validation():
        raise ValidationException(detail="Invalid email format")

    @app.get("/error/not-found")
    def trigger_not_found():
        raise ResourceNotFoundException(detail="User record not found")

    @app.get("/error/unauthorized")
    def trigger_unauthorized():
        raise UnauthorizedException(detail="Token expired")

    @app.get("/error/unhandled")
    def trigger_unhandled():
        raise ValueError("Database connection dropped unexpectedly")

    return TestClient(app, raise_server_exceptions=False)

def test_validation_exception_handler():
    """Ensure custom ValidationException yields the exact error object."""
    client = create_exception_test_client()
    response = client.get("/error/validation")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value

    data = response.json()
    assert "error" in data
    assert data["detail"] == "Invalid email format"
    assert data["error"] == "VALIDATION_ERROR"
    assert data["status_code"] == HTTPStatus.UNPROCESSABLE_ENTITY.value


def test_resource_not_found_exception_handler():
    """Ensure missing resources yield a clean 404 Not Found error state."""
    client = create_exception_test_client()
    response = client.get("/error/not-found")

    assert response.status_code == HTTPStatus.NOT_FOUND.value

    data = response.json()
    assert "error" in data
    assert data["detail"] == "User record not found"
    assert data["error"] == "NOT_FOUND"
    assert data["status_code"] == HTTPStatus.NOT_FOUND.value


def test_unauthorized_exception_handler():
    """Ensure security failures default cleanly to a 401 Unauthorized status."""
    client = create_exception_test_client()
    response = client.get("/error/unauthorized")

    assert response.status_code == HTTPStatus.UNAUTHORIZED.value

    data = response.json()
    assert "error" in data
    assert data["detail"] == "Token expired"
    assert data["error"] == "UNAUTHORIZED"
    assert data["status_code"] == HTTPStatus.UNAUTHORIZED.value


def test_unhandled_native_exception_handler():
    """Ensure regular Python exceptions are captured safely under a 500 block."""
    client = create_exception_test_client()
    response = client.get("/error/unhandled")

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value

    data = response.json()
    assert "error" in data
    assert data["error"] == "INTERNAL_ERROR"
    assert data["detail"] == "An unexpected error occurred"
    assert data["status_code"] == HTTPStatus.INTERNAL_SERVER_ERROR.value
