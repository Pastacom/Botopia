import pytest
from uuid import uuid4

from src.repositories.lock_repository import LockRepository


@pytest.mark.asyncio
async def test_toggle_lock_acquire(mock_session_builder, mock_session):
    user_id = uuid4()

    await LockRepository.toggle_user_lock(mock_session_builder, user_id, should_lock=True)

    assert mock_session.execute.called
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_toggle_lock_release(mock_session_builder, mock_session):
    user_id = uuid4()

    await LockRepository.toggle_user_lock(mock_session_builder, user_id, should_lock=False)

    assert mock_session.execute.called
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_toggle_lock_multiple_users(mock_session_builder, mock_session):
    user_id1 = uuid4()
    user_id2 = uuid4()

    await LockRepository.toggle_user_lock(mock_session_builder, user_id1, should_lock=True)
    await LockRepository.toggle_user_lock(mock_session_builder, user_id2, should_lock=True)

    assert mock_session.commit.call_count == 2
