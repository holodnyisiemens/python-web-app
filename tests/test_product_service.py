import json
from unittest.mock import AsyncMock, Mock

import pytest
from redis.asyncio import Redis

from src.repositories.product_repository import ProductRepository
from src.schemas import ProductAddDTO, ProductDTO
from src.services.product_service import ProductService

product_data = ProductAddDTO(
    title="example",
    price=1000,
    stock_qty=10,
)


class TestProductService:
    @pytest.mark.asyncio
    async def test_create_product(self, redis: Redis):
        # мокаем репозиторий и объекты в нем
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_product_repo.session = Mock()
        mock_product_repo.session.commit = AsyncMock()
        mock_product_repo.session.rollback = AsyncMock()

        # то, что вернёт create()
        mock_product_repo.create.return_value = {
            "id": 1,
            "title": "example",
            "price": 1000,
            "stock_qty": 10,
        }

        product_service = ProductService(product_repo=mock_product_repo, redis=redis)
        result = await product_service.create(product_data)

        # проверка что для асинхронного метода create() был всего 1 await и с указанным объектом
        mock_product_repo.create.assert_awaited_once_with(product_data)
        mock_product_repo.session.commit.assert_awaited_once()
        assert isinstance(result, ProductDTO)
        assert result.title == "example"

    @pytest.mark.asyncio
    async def test_delete_product(self, redis: Redis):
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_product_repo.session = Mock()
        mock_product_repo.session.commit = AsyncMock()
        mock_product_repo.session.rollback = AsyncMock()

        product_id = 1

        fake_product = Mock(id=product_id, title="example", price=1000, stock_qty=10)
        mock_product_repo.get_by_id.return_value = fake_product

        mock_product_repo.delete.return_value = None

        product_service = ProductService(product_repo=mock_product_repo, redis=redis)
        result = await product_service.delete(product_id)

        assert result is None

        mock_product_repo.get_by_id.assert_awaited_once_with(product_id)
        mock_product_repo.delete.assert_awaited_once_with(fake_product)
        mock_product_repo.session.commit.assert_awaited_once()

        # rollback не должен быть вызван
        mock_product_repo.session.rollback.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_by_id_cache_hit(self, redis: Redis):
        # подготовка: данные уже есть в кэше
        product_id = 1
        cached = {"id": product_id, "title": "test", "price": "1000", "stock_qty": "10"}
        await redis.set(f"product:{product_id}", json.dumps(cached))

        mock_product_repo = AsyncMock()
        product_service = ProductService(product_repo=mock_product_repo, redis=redis)

        result = await product_service.get_by_id(product_id)

        # данные вернулись из кэша
        assert result.id == product_id
        assert result.title == "test"

        # метод репозитория не вызывался
        mock_product_repo.get_by_id.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_get_by_id_cache_miss(self, redis: Redis):
        # подготовка: кэша нет
        product_id = 2
        mock_product_repo = AsyncMock()
        fake_product = {
            "id": product_id,
            "title": "test",
            "price": "1000",
            "stock_qty": "10",
        }
        mock_product_repo.get_by_id.return_value = fake_product

        product_service = ProductService(product_repo=mock_product_repo, redis=redis)

        result = await product_service.get_by_id(product_id)

        assert result.id == product_id
        assert result.title == "test"

        # метод репозитория был вызван
        mock_product_repo.get_by_id.assert_awaited_once_with(product_id)

        # данные должны оказаться в кэше
        cached = await redis.get(f"product:{product_id}")
        assert cached is not None
        cached_data = json.loads(cached)
        assert cached_data["title"] == "test"
