from uuid import UUID

from fastapi import APIRouter, Body, Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.db.database import get_db
from src.services.lock_service import LockService

router = APIRouter(prefix='/lock', tags=['lock'])


@router.post('/acquire_lock')
async def acquire_lock_handler(user_id: Annotated[UUID, Body(embed=True)],
                               lock_service: Annotated[LockService, Depends()],
                               session_builder: async_sessionmaker[AsyncSession] = Depends(get_db)):
    await lock_service.acquire_lock(session_builder, user_id)


@router.post('/release_lock')
async def release_lock_handler(user_id: Annotated[UUID, Body(embed=True)],
                               lock_service: Annotated[LockService, Depends()],
                               session_builder: async_sessionmaker[AsyncSession] = Depends(get_db)):
    await lock_service.release_lock(session_builder, user_id)
