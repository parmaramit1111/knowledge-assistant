import uuid
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.core.middleware.request_id import RequestIdMiddleware, REQUEST_ID_HEADER_NAME

# Helper to spin up a clean test instance
def create_test_app():
    test_app = FastAPI()
    test_app.add_middleware(RequestIdMiddleware)

    @test_app.get("/")
    def index():
        return {"status": "ok"}

    return TestClient(test_app)

def test_middleware_uses_provided_request_id():
    client = create_test_app()
    custom_id = str(uuid.uuid4())

    # Send request with a pre-defined request ID
    response = client.get("/", headers={REQUEST_ID_HEADER_NAME: custom_id})

    assert response.status_code == 200
    assert REQUEST_ID_HEADER_NAME in response.headers
    # Assert exact equality instead of >=
    assert response.headers[REQUEST_ID_HEADER_NAME] == custom_id

def test_middleware_generates_new_id_if_missing():
    client = create_test_app()

    # Send request WITHOUT the header
    response = client.get("/")

    assert response.status_code == 200
    assert REQUEST_ID_HEADER_NAME in response.headers

    # Verify that the generated value is a valid UUID
    generated_id = response.headers[REQUEST_ID_HEADER_NAME]
    try:
        uuid.UUID(generated_id, version=4)
    except ValueError:
        assert False, f"Returned header {generated_id} is not a valid UUIDv4"
