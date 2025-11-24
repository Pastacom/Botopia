from fastapi import APIRouter, Body, Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.db.database import get_db
from src.schemas.Request.GetUsersRequest import GetUsersRequest
from src.schemas.Request.CreateUsersRequest import CreateUsersRequest
from src.schemas.Response.GetUsersResponse import GetUsersResponse
from src.services.users_service import UserService

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/create_user')
async def create_user_handler(user: CreateUsersRequest, user_service: Annotated[UserService, Depends()],
                              session_builder: async_sessionmaker[AsyncSession] = Depends(get_db)):
    await user_service.create_users(session_builder, [user])


@router.post('/create_users')
async def create_users_handler(users: Annotated[list[CreateUsersRequest], Body(embed=True)],
                               user_service: Annotated[UserService, Depends()],
                               session_builder: async_sessionmaker[AsyncSession] = Depends(get_db)):
    await user_service.create_users(session_builder, users)


@router.post('/get_users', response_model=list[GetUsersResponse])
async def get_users_handler(user_filters: GetUsersRequest,
                            user_service: Annotated[UserService, Depends()],
                            session_builder: async_sessionmaker[AsyncSession] = Depends(get_db)):
    return await user_service.get_users(session_builder, user_filters)
