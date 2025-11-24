from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(
    settings.DATABASE_URL_ASYNCPG,
    echo=False,
)


sync_engine = create_engine(
    settings.DATABASE_URL_PSYCOPG,
    echo=False,
)


async_session_factory = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


session_factory = sessionmaker(sync_engine)
