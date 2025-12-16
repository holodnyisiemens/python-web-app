from typing import AsyncGenerator

from litestar import Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_factory
from src.repositories.address_repository import AddressRepository
from src.repositories.cart_repository import CartRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.report_repository import ReportRepository
from src.repositories.user_repository import UserRepository
from src.services.cart_service import CartService
from src.services.report_service import ReportService
from src.services.user_service import UserService


async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Провайдер сессии базы данных"""
    async with async_session_factory() as session:
        yield session


async def provide_redis(request: Request) -> Redis:
    """Провайдер клиента Redis"""
    return request.app.state.redis


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    """Провайдер репозитория пользователей"""
    return UserRepository(session=db_session)


async def provide_user_service(
    user_repository: UserRepository, redis: Redis
) -> UserService:
    """Провайдер сервиса пользователей"""
    return UserService(user_repository, redis)


async def provide_cart_repository(db_session: AsyncSession) -> CartRepository:
    """Провайдер репозитория корзины"""
    return CartRepository(session=db_session)


async def provide_cart_service(
    cart_repo: CartRepository,
    user_repo: UserRepository,
    address_repo: AddressRepository,
    product_repo: ProductRepository,
) -> CartService:
    """Провайдер сервиса корзины"""
    return CartService(cart_repo, user_repo, address_repo, product_repo)


async def provide_report_repository(db_session: AsyncSession) -> ReportRepository:
    """Провайдер репозитория отчетов"""
    return ReportRepository(session=db_session)


async def provide_report_service(report_repo: ReportRepository) -> ReportService:
    """Провайдер сервиса создания отчетов"""
    return ReportService(report_repo=report_repo)
