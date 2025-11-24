import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


load_dotenv()

engine = create_async_engine(os.getenv("DATABASE_URL"))

AsyncSessionMaker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> async_sessionmaker[AsyncSession] | None:
    return AsyncSessionMaker
