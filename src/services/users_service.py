from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.exceptions.exceptions import UserAlreadyExistsException, UserNotFoundException
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.schemas.Request.CreateUsersRequest import CreateUsersRequest
from src.schemas.Request.GetUsersRequest import GetUsersRequest
from src.schemas.Response.GetUsersResponse import GetUsersResponse
from src.utils.utils import hash_password


class UserService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends()]):
        self._user_repository = user_repository

    async def create_users(self, session_builder: async_sessionmaker[AsyncSession], users: list[CreateUsersRequest]):
        logins = [user.login for user in users]

        existing_logins = await self._user_repository.check_existing_logins(session_builder, logins)

        if len(existing_logins) != 0:
            raise UserAlreadyExistsException(message='User already exists', meta={'existing_logins': existing_logins})

        users = list(map(lambda user: User(login=user.login, hashed_password=hash_password(user.password),
                                           project_id=user.project_id, env=user.env, domain=user.domain), users))

        return await self._user_repository.add_users(session_builder, users)

    async def get_users(self, session_builder: async_sessionmaker[AsyncSession],
                        user_filters: GetUsersRequest) -> list[GetUsersResponse]:
        """
        Function prioritizes some filters over the others.
        If user id is passed, will return one user with such id and stop
        If user login is passed, will return one user with such login and stop
        Otherwise will filter users by all other passed params and return valid users
        :param session_builder: db session maker
        :param user_filters: filters to use during user selection
        :return: list of users that passed all filters
        """

        if user_filters.id is not None:
            found_user = await self._user_repository.get_by_id(session_builder, user_filters.id)

            if found_user is None:
                raise UserNotFoundException(message='User not found', meta={'id': str(user_filters.id)})

            return [GetUsersResponse.model_validate(found_user, from_attributes=True)]

        if user_filters.login is not None:
            found_user = await self._user_repository.get_by_login(session_builder, user_filters.login)

            if found_user is None:
                raise UserNotFoundException(message='User not found', meta={'login': user_filters.id})

            return [GetUsersResponse.model_validate(found_user, from_attributes=True)]

        users = await self._user_repository.get_filtered_users(session_builder, project_id=user_filters.project_id,
                                                               env=user_filters.env,
                                                               domain=user_filters.domain,
                                                               only_available=user_filters.only_available)

        return list(map(lambda user: GetUsersResponse.model_validate(user, from_attributes=True), users))
