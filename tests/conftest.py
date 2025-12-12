from unittest.mock import AsyncMock

import pytest
from litestar import Litestar
from litestar.di import Provide
from litestar.testing import AsyncTestClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import settings
from controllers.cart_controller import CartController
from controllers.user_controller import UserController
from database import Base
from repositories.address_repository import AddressRepository
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository
from schemas import (
    AddressAddDTO,
    AddressDTO,
    CartAddDTO,
    CartDTO,
    ProductAddDTO,
    ProductDTO,
    UserAddDTO,
    UserDTO,
)
from services.cart_service import CartService
from services.user_service import UserService

TEST_DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD.get_secret_value()}@{settings.DB_HOST}:{settings.DB_PORT}/test_db"


@pytest.fixture()
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture()
async def tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session(engine, tables):
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest.fixture
async def user_repository(session):
    return UserRepository(session)


@pytest.fixture
async def product_repository(session):
    return ProductRepository(session)


@pytest.fixture
async def address_repository(session):
    return AddressRepository(session)


@pytest.fixture
async def cart_repository(session):
    return CartRepository(session)


@pytest.fixture
async def mock_user_service():
    return AsyncMock(spec=UserService)


@pytest.fixture
async def mock_cart_service():
    return AsyncMock(spec=CartService)


@pytest.fixture
async def client(
    mock_user_service, user_repository, mock_cart_service, cart_repository
):
    app = Litestar(
        route_handlers=[UserController, CartController],
        dependencies={
            "user_repository": Provide(lambda: user_repository, sync_to_thread=False),
            "user_service": Provide(lambda: mock_user_service, sync_to_thread=False),
            "cart_repository": Provide(lambda: cart_repository, sync_to_thread=False),
            "cart_service": Provide(lambda: mock_cart_service, sync_to_thread=False),
        },
    )
    async with AsyncTestClient(app) as client:
        yield client


# фикстуры с тестовыми данными: до и после создания объектов по-отдельности
@pytest.fixture
async def user_data_1() -> UserAddDTO:
    return UserAddDTO(
        username="Alexey",
        email="email@example.com",
    )


@pytest.fixture
async def user_1(user_repository: UserRepository, user_data_1: UserAddDTO) -> UserDTO:
    return await user_repository.create(user_data_1)


@pytest.fixture
async def user_data_2() -> UserAddDTO:
    return UserAddDTO(
        username="Alexander",
        email="test@example.com",
    )


@pytest.fixture
async def user_2(user_repository: UserRepository, user_data_2: UserAddDTO) -> UserDTO:
    return await user_repository.create(user_data_2)


@pytest.fixture
async def address_data_1(user_1: UserDTO) -> AddressAddDTO:
    return AddressAddDTO(
        user_id=user_1.id,
        street="Lenina",
        city="Ekb",
        country="Russia",
    )


@pytest.fixture
async def address_1(
    address_repository: AddressRepository, address_data_1: AddressAddDTO
) -> AddressDTO:
    return await address_repository.create(address_data_1)


@pytest.fixture
async def address_data_2(user_2: UserDTO) -> AddressAddDTO:
    return AddressAddDTO(
        user_id=user_2.id,
        street="Mira",
        city="Ekb",
        country="Russia",
    )


@pytest.fixture
async def address_2(
    address_repository: AddressRepository, address_data_2: AddressAddDTO
) -> AddressDTO:
    return await address_repository.create(address_data_2)


@pytest.fixture
async def cart_data_1(address_1: AddressDTO) -> CartAddDTO:
    return CartAddDTO(
        customer_id=address_1.user_id,
        delivery_address_id=address_1.id,
    )


@pytest.fixture
async def cart_1(cart_repository: CartRepository, cart_data_1: CartAddDTO) -> CartDTO:
    return await cart_repository.create(cart_data_1)


@pytest.fixture
async def cart_data_2(address_2: AddressDTO) -> CartAddDTO:
    return CartAddDTO(
        customer_id=address_2.user_id,
        delivery_address_id=address_2.id,
    )


@pytest.fixture
async def cart_2(cart_repository: CartRepository, cart_data_2: CartAddDTO) -> CartDTO:
    return await cart_repository.create(cart_data_2)


@pytest.fixture
async def product_data_1() -> ProductAddDTO:
    return ProductAddDTO(
        title="Headphones",
        price=999.50,
        stock_qty=2,
    )


@pytest.fixture
async def product_1(
    product_repository: ProductRepository, product_data_1: ProductAddDTO
) -> ProductDTO:
    return await product_repository.create(product_data_1)


@pytest.fixture
async def product_data_2() -> ProductAddDTO:
    return ProductAddDTO(
        title="JBL",
        price=1500,
        stock_qty=0,
    )


@pytest.fixture
async def product_2(
    product_repository: ProductRepository, product_data_2: ProductAddDTO
) -> ProductDTO:
    return await product_repository.create(product_data_2)
