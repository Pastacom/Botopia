import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schemas.Shared.Domain import Domain
from src.schemas.Shared.Environment import Environment
from src.repositories.user_repository import UserRepository
from src.repositories.lock_repository import LockRepository
from src.services.users_service import UserService
from src.services.lock_service import LockService


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.add_all = MagicMock()
    session.add = MagicMock()
    return session


@pytest.fixture
def mock_session_builder(mock_session):
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)
    
    builder = MagicMock()
    builder.return_value = mock_session
    
    return builder


@pytest.fixture
def generated_user_id():
    return uuid4()


@pytest.fixture
def generated_project_id():
    return uuid4()


@pytest.fixture
def sample_user(generated_user_id, generated_project_id):
    return User(
        id=generated_user_id,
        login="test_user",
        hashed_password="hashed_password_123",
        project_id=generated_project_id,
        env=Environment.PROD,
        domain=Domain.REGULAR,
        created_at=datetime.now(timezone.utc),
        locktime=None
    )


@pytest.fixture
def locked_user(generated_user_id, generated_project_id):
    return User(
        id=generated_user_id,
        login="locked_user",
        hashed_password="hashed_password_311",
        project_id=generated_project_id,
        env=Environment.PROD,
        domain=Domain.CANARY,
        created_at=datetime.now(timezone.utc),
        locktime=datetime.now(timezone.utc)
    )


@pytest.fixture
def user_repository():
    return UserRepository()


@pytest.fixture
def user_service(user_repository):
    return UserService(user_repository=user_repository)


@pytest.fixture
def lock_repository():
    return LockRepository()


@pytest.fixture
def lock_service(lock_repository, user_repository):
    return LockService(
        lock_repository=lock_repository,
        user_repository=user_repository
    )


@pytest.fixture
def mock_user_service():
    service = MagicMock(spec=UserService)
    service.create_users = AsyncMock()
    service.get_users = AsyncMock(return_value=[])
    return service


@pytest.fixture
def mock_lock_service():
    service = MagicMock(spec=LockService)
    service.acquire_lock = AsyncMock()
    service.release_lock = AsyncMock()
    return service
