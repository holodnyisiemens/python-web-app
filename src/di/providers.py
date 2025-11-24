from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session_factory
from repositories.user_repository import UserRepository
from services.user_service import UserService


async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Провайдер сессии базы данных"""
    async with async_session_factory() as session:
        yield session


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    """Провайдер репозитория пользователей"""
    return UserRepository(db_session)


async def provide_user_service(user_repository: UserRepository) -> UserService:
    """Провайдер сервиса пользователей"""
    return UserService(user_repository)
