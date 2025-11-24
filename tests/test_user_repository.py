import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.repositories.user_repository import UserRepository


@pytest.mark.asyncio
async def test_get_by_id_found(mock_session_builder, mock_session, sample_user):
    user_id = sample_user.id
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = sample_user
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await UserRepository.get_by_id(mock_session_builder, user_id)
    
    assert result == sample_user
    assert result.id == user_id


@pytest.mark.asyncio
async def test_get_by_id_not_found(mock_session_builder, mock_session):
    user_id = uuid4()
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await UserRepository.get_by_id(mock_session_builder, user_id)
    
    assert result is None


@pytest.mark.asyncio
async def test_get_by_login_found(mock_session_builder, mock_session, sample_user):
    login = sample_user.login
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = sample_user
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await UserRepository.get_by_login(mock_session_builder, login)
    
    assert result == sample_user
    assert result.login == login


@pytest.mark.asyncio
async def test_get_by_login_not_found(mock_session_builder, mock_session):
    login = "non_existent_user"
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await UserRepository.get_by_login(mock_session_builder, login)
    
    assert result is None


@pytest.mark.asyncio
async def test_get_filtered_users_no_filters(mock_session_builder, mock_session, sample_user):
    users = [sample_user]
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = users
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    repository = UserRepository()
    result = await repository.get_filtered_users(mock_session_builder)
    
    assert result == users
    assert len(result) == 1


@pytest.mark.asyncio
async def test_get_filtered_users_with_project_id(mock_session_builder, mock_session, sample_user):
    project_id = sample_user.project_id
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [sample_user]
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    repository = UserRepository()
    result = await repository.get_filtered_users(
        mock_session_builder,
        project_id=project_id
    )
    
    assert len(result) == 1
    assert result[0].project_id == project_id


@pytest.mark.asyncio
async def test_get_filtered_users_with_env(mock_session_builder, mock_session, sample_user):
    env = sample_user.env
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [sample_user]
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    repository = UserRepository()
    result = await repository.get_filtered_users(
        mock_session_builder,
        env=env
    )
    
    assert len(result) == 1
    assert result[0].env == env


@pytest.mark.asyncio
async def test_get_filtered_users_with_domain(mock_session_builder, mock_session, sample_user):
    domain = sample_user.domain
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [sample_user]
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    repository = UserRepository()
    result = await repository.get_filtered_users(
        mock_session_builder,
        domain=domain
    )
    
    assert len(result) == 1
    assert result[0].domain == domain


@pytest.mark.asyncio
async def test_get_filtered_users_only_available(mock_session_builder, mock_session, sample_user):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [sample_user]
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    repository = UserRepository()
    result = await repository.get_filtered_users(
        mock_session_builder,
        only_available=True
    )
    
    assert len(result) == 1
    assert result[0].locktime is None


@pytest.mark.asyncio
async def test_get_filtered_users_all_filters(mock_session_builder, mock_session, sample_user):
    project_id = sample_user.project_id
    env = sample_user.env
    domain = sample_user.domain
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [sample_user]
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    repository = UserRepository()
    result = await repository.get_filtered_users(
        mock_session_builder,
        project_id=project_id,
        env=env,
        domain=domain,
        only_available=True
    )
    
    assert len(result) == 1


@pytest.mark.asyncio
async def test_add_users(mock_session_builder, mock_session, sample_user):
    users = [sample_user]
    
    await UserRepository.add_users(mock_session_builder, users)
    
    mock_session.add_all.assert_called_once_with(users)
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_check_existing_logins_found(mock_session_builder, mock_session):
    logins = ["user1", "user2", "user3"]
    existing_logins = ["user1", "user3"]
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = existing_logins
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await UserRepository.check_existing_logins(mock_session_builder, logins)
    
    assert result == existing_logins
    assert len(result) == 2


@pytest.mark.asyncio
async def test_check_existing_logins_not_found(mock_session_builder, mock_session):
    logins = ["new_user1", "new_user2"]
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await UserRepository.check_existing_logins(mock_session_builder, logins)
    
    assert result == []
    assert len(result) == 0
