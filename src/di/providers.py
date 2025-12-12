from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session_factory
from repositories.address_repository import AddressRepository
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository
from services.cart_service import CartService
from services.user_service import UserService


async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Провайдер сессии базы данных"""
    async with async_session_factory() as session:
        yield session


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    """Провайдер репозитория пользователей"""
    return UserRepository(session=db_session)


async def provide_user_service(user_repository: UserRepository) -> UserService:
    """Провайдер сервиса пользователей"""
    return UserService(user_repo=user_repository)


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
