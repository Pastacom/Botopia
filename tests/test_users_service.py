import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from src.exceptions.exceptions import UserAlreadyExistsException, UserNotFoundException
from src.schemas.Request.CreateUsersRequest import CreateUsersRequest
from src.schemas.Request.GetUsersRequest import GetUsersRequest
from src.schemas.Shared.Domain import Domain
from src.schemas.Shared.Environment import Environment


@pytest.mark.asyncio
async def test_create_users_success(user_service, mock_session_builder, mock_session):
    project_id = uuid4()
    users_request = [
        CreateUsersRequest(
            login="user1",
            password="password1",
            project_id=project_id,
            env=Environment.STAGE,
            domain=Domain.REGULAR
        ),
        CreateUsersRequest(
            login="user2",
            password="password2",
            project_id=project_id,
            env=Environment.PROD,
            domain=Domain.CANARY
        )
    ]
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    with patch('src.services.users_service.hash_password') as mock_hash:
        mock_hash.side_effect = lambda p: f"hashed_{p}"
        
        await user_service.create_users(mock_session_builder, users_request)
    
    assert mock_session.add_all.called
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_users_user_already_exists(user_service, mock_session_builder, mock_session):
    project_id = uuid4()
    users_request = [
        CreateUsersRequest(
            login="existing_user",
            password="password1",
            project_id=project_id,
            env=Environment.STAGE,
            domain=Domain.REGULAR
        )
    ]
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = ["existing_user"]
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    with pytest.raises(UserAlreadyExistsException) as exc_info:
        await user_service.create_users(mock_session_builder, users_request)
    
    assert exc_info.value.status_code == 409
    assert "existing_logins" in exc_info.value.meta


@pytest.mark.asyncio
async def test_get_users_by_id_found(user_service, mock_session_builder, mock_session, sample_user):
    user_filters = GetUsersRequest(id=sample_user.id)
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = sample_user
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await user_service.get_users(mock_session_builder, user_filters)
    
    assert len(result) == 1
    assert result[0].id == sample_user.id
    assert result[0].login == sample_user.login


@pytest.mark.asyncio
async def test_get_users_by_id_not_found(user_service, mock_session_builder, mock_session):
    user_id = uuid4()
    user_filters = GetUsersRequest(id=user_id)
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    with pytest.raises(UserNotFoundException) as exc_info:
        await user_service.get_users(mock_session_builder, user_filters)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.meta["id"] == str(user_id)


@pytest.mark.asyncio
async def test_get_users_by_login_found(user_service, mock_session_builder, mock_session, sample_user):
    user_filters = GetUsersRequest(login=sample_user.login)
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = sample_user
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await user_service.get_users(mock_session_builder, user_filters)
    
    assert len(result) == 1
    assert result[0].login == sample_user.login


@pytest.mark.asyncio
async def test_get_users_by_login_not_found(user_service, mock_session_builder, mock_session):
    login = "non_existent_user"
    user_filters = GetUsersRequest(login=login)
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    with pytest.raises(UserNotFoundException) as exc_info:
        await user_service.get_users(mock_session_builder, user_filters)
    
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_get_users_with_filters(user_service, mock_session_builder, mock_session, sample_user):
    user_filters = GetUsersRequest(
        project_id=sample_user.project_id,
        env=sample_user.env,
        domain=sample_user.domain,
        only_available=True
    )
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [sample_user]
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await user_service.get_users(mock_session_builder, user_filters)
    
    assert len(result) == 1
    assert result[0].project_id == sample_user.project_id
    assert result[0].env == sample_user.env.value
    assert result[0].domain == sample_user.domain.value


@pytest.mark.asyncio
async def test_get_users_no_filters(user_service, mock_session_builder, mock_session, sample_user):
    user_filters = GetUsersRequest()
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [sample_user]
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await user_service.get_users(mock_session_builder, user_filters)
    
    assert len(result) == 1


@pytest.mark.asyncio
async def test_get_users_priority_id_over_login(user_service, mock_session_builder, mock_session, sample_user):
    user_filters = GetUsersRequest(
        id=sample_user.id,
        login="different_login"
    )
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = sample_user
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await user_service.get_users(mock_session_builder, user_filters)
    
    assert len(result) == 1
    assert result[0].id == sample_user.id
