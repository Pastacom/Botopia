from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.exceptions.exceptions import UserNotFoundException, UserIsAlreadyLockedException
from src.repositories.lock_repository import LockRepository
from src.repositories.user_repository import UserRepository


class LockService:
    def __init__(self, lock_repository: Annotated[LockRepository, Depends()],
                 user_repository: Annotated[UserRepository, Depends()]):
        self._lock_repository = lock_repository
        self._user_repository = user_repository

    async def acquire_lock(self, session_builder: async_sessionmaker[AsyncSession], user_id: UUID):
        user = await self._user_repository.get_by_id(session_builder, user_id)

        if user is None:
            raise UserNotFoundException(message='User not found', meta={'id': str(user_id)})

        if user.locktime is not None:
            raise UserIsAlreadyLockedException(message='User is already locked by someone else',
                                               meta={'id': str(user_id), 'locktime': user.locktime.isoformat()})

        await self._lock_repository.toggle_user_lock(session_builder, user_id, should_lock=True)

    async def release_lock(self, session_builder: async_sessionmaker[AsyncSession], user_id: UUID):
        user = await self._user_repository.get_by_id(session_builder, user_id)

        if user is None:
            raise UserNotFoundException(message='User not found', meta={'id': str(user_id)})

        await self._lock_repository.toggle_user_lock(session_builder, user_id, should_lock=False)
