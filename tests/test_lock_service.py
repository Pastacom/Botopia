import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.exceptions.exceptions import UserNotFoundException, UserIsAlreadyLockedException


@pytest.mark.asyncio
async def test_acquire_lock_success(lock_service, mock_session_builder, mock_session, sample_user):
    user_id = sample_user.id

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = sample_user
    mock_session.execute = AsyncMock(return_value=mock_result)

    await lock_service.acquire_lock(mock_session_builder, user_id)

    assert mock_session.execute.call_count >= 1
    mock_session.commit.assert_called()


@pytest.mark.asyncio
async def test_acquire_lock_user_not_found(lock_service, mock_session_builder, mock_session):
    user_id = uuid4()

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    with pytest.raises(UserNotFoundException) as exc_info:
        await lock_service.acquire_lock(mock_session_builder, user_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.meta["id"] == str(user_id)


@pytest.mark.asyncio
async def test_acquire_lock_user_already_locked(lock_service, mock_session_builder, mock_session, locked_user):
    user_id = locked_user.id

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = locked_user
    mock_session.execute = AsyncMock(return_value=mock_result)

    with pytest.raises(UserIsAlreadyLockedException) as exc_info:
        await lock_service.acquire_lock(mock_session_builder, user_id)

    assert exc_info.value.status_code == 409
    assert exc_info.value.meta["id"] == str(user_id)
    assert "locktime" in exc_info.value.meta


@pytest.mark.asyncio
async def test_release_lock_success(lock_service, mock_session_builder, mock_session, locked_user):
    user_id = locked_user.id

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = locked_user
    mock_session.execute = AsyncMock(return_value=mock_result)

    await lock_service.release_lock(mock_session_builder, user_id)

    assert mock_session.execute.call_count >= 1
    mock_session.commit.assert_called()


@pytest.mark.asyncio
async def test_release_lock_user_not_found(lock_service, mock_session_builder, mock_session):
    user_id = uuid4()

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    with pytest.raises(UserNotFoundException) as exc_info:
        await lock_service.release_lock(mock_session_builder, user_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.meta["id"] == str(user_id)


@pytest.mark.asyncio
async def test_release_lock_unlocked_user(lock_service, mock_session_builder, mock_session, sample_user):
    user_id = sample_user.id

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = sample_user
    mock_session.execute = AsyncMock(return_value=mock_result)

    await lock_service.release_lock(mock_session_builder, user_id)

    assert mock_session.execute.call_count >= 1
    mock_session.commit.assert_called()
