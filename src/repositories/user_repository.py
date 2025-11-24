from uuid import UUID

from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.models.user import User
from src.schemas.Shared.Domain import Domain
from src.schemas.Shared.Environment import Environment


class UserRepository:
    @staticmethod
    async def _build_query(project_id: UUID | None = None, env: Environment | None = None,
                           domain: Domain | None = None, only_available: bool = False) -> Select[tuple[User]]:
        query = select(User)

        if project_id is not None:
            query = query.where(User.project_id == project_id)

        if env is not None:
            query = query.where(User.env == env)

        if domain is not None:
            query = query.where(User.domain == domain)

        if only_available:
            query = query.where(User.locktime.is_(None))

        return query

    @staticmethod
    async def get_by_id(session_builder: async_sessionmaker[AsyncSession], user_id: UUID) -> User | None:
        async with session_builder() as session:
            query = select(User).where(User.id == user_id)

            result = await session.execute(query)

            return result.scalar_one_or_none()

    @staticmethod
    async def get_by_login(session_builder: async_sessionmaker[AsyncSession], login: str) -> User | None:
        async with session_builder() as session:
            query = select(User).where(User.login == login)

            result = await session.execute(query)

            return result.scalar_one_or_none()

    async def get_filtered_users(self, session_builder: async_sessionmaker[AsyncSession],
                                 project_id: UUID | None = None, env: Environment | None = None,
                                 domain: Domain | None = None, only_available: bool = False) -> list[User]:
        async with session_builder() as session:
            query = await self._build_query(project_id=project_id, env=env,
                                            domain=domain, only_available=only_available)

            result = await session.execute(query)

            return result.scalars().all()

    @staticmethod
    async def add_users(session_builder: async_sessionmaker[AsyncSession], users: list[User]):
        async with session_builder() as session:
            session.add_all(users)
            await session.commit()

    @staticmethod
    async def check_existing_logins(session_builder: async_sessionmaker[AsyncSession], logins: list[str]) -> list[str]:
        async with session_builder() as session:
            query = select(User.login).where(User.login.in_(logins))

            result = await session.execute(query)

            return result.scalars().all()
