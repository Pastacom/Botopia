import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from uuid import uuid4

from src.handlers.main import app
from src.db.database import get_db
from src.services.users_service import UserService


@pytest.fixture
def client(mock_session_builder, mock_user_service):
    app.dependency_overrides[get_db] = lambda: mock_session_builder
    app.dependency_overrides[UserService] = lambda: mock_user_service

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def sample_project_id():
    return uuid4()


@pytest.fixture
def create_user_request(sample_project_id):
    return {
        "login": "test_user",
        "password": "test_password",
        "project_id": str(sample_project_id),
        "env": "stage",
        "domain": "regular"
    }


@pytest.fixture
def create_users_request(sample_project_id):
    return {
        "users": [
            {
                "login": "user1",
                "password": "password1",
                "project_id": str(sample_project_id),
                "env": "stage",
                "domain": "regular"
            },
            {
                "login": "user2",
                "password": "password2",
                "project_id": str(sample_project_id),
                "env": "prod",
                "domain": "canary"
            }
        ]
    }


def test_create_user_endpoint(client, create_user_request, mock_user_service, mock_session_builder):
    response = client.post("/api/v1/users/create_user", json=create_user_request)
    
    assert response.status_code == 200
    mock_user_service.create_users.assert_called_once()


def test_create_users_endpoint(client, create_users_request, mock_user_service, mock_session_builder):
    response = client.post("/api/v1/users/create_users", json=create_users_request)
    
    assert response.status_code == 200
    mock_user_service.create_users.assert_called_once()


def test_get_users_endpoint(client, sample_project_id, mock_user_service, mock_session_builder):
    get_users_request = {
        "project_id": str(sample_project_id),
        "env": "stage",
        "domain": "regular",
        "only_available": True
    }
    
    response = client.post("/api/v1/users/get_users", json=get_users_request)
    
    assert response.status_code == 200
    mock_user_service.get_users.assert_called_once()


def test_get_users_endpoint_with_id(client, mock_user_service, mock_session_builder):
    user_id = uuid4()
    get_users_request = {
        "id": str(user_id)
    }
    
    response = client.post("/api/v1/users/get_users", json=get_users_request)
    
    assert response.status_code == 200
    mock_user_service.get_users.assert_called_once()


def test_get_users_endpoint_with_login(client, mock_user_service, mock_session_builder):
    get_users_request = {
        "login": "pickle-rick!"
    }

    response = client.post("/api/v1/users/get_users", json=get_users_request)

    assert response.status_code == 200
    mock_user_service.get_users.assert_called_once()
