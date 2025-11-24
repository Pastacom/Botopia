import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from src.handlers.main import app
from src.db.database import get_db
from src.services.lock_service import LockService


@pytest.fixture
def client(mock_session_builder, mock_lock_service):
    app.dependency_overrides[get_db] = lambda: mock_session_builder
    app.dependency_overrides[LockService] = lambda: mock_lock_service

    yield TestClient(app)

    app.dependency_overrides.clear()


def test_acquire_lock_endpoint(client, mock_lock_service, mock_session_builder):
    user_id = uuid4()
    request_body = {"user_id": str(user_id)}

    response = client.post("/api/v1/lock/acquire_lock", json=request_body)

    assert response.status_code == 200
    mock_lock_service.acquire_lock.assert_called_once()


def test_release_lock_endpoint(client, mock_lock_service, mock_session_builder):
    user_id = uuid4()
    request_body = {"user_id": str(user_id)}

    response = client.post("/api/v1/lock/release_lock", json=request_body)

    assert response.status_code == 200
    mock_lock_service.release_lock.assert_called_once()
