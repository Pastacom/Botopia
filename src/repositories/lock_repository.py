from datetime import datetime, timezone
from uuid import UUID

from fastapi import Depends
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.models.user import User


class LockRepository:
    @staticmethod
    async def toggle_user_lock(session_builder: async_sessionmaker[AsyncSession],
                               user_id: UUID, should_lock: bool = True):
        async with session_builder() as session:
            query = update(User).where(User.id == user_id).values(
                locktime=datetime.now(timezone.utc) if should_lock else None)

            await session.execute(query)
            await session.commit()