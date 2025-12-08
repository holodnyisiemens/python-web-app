import pytest
from litestar.testing import AsyncTestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker

from config import settings
from database import Base
from main import app
from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository
from repositories.cart_repository import CartRepository
from repositories.address_repository import AddressRepository


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
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
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
async def client():
    async with AsyncTestClient(app=app) as client:
        yield client
