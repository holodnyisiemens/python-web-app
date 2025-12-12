from unittest.mock import AsyncMock, Mock

import pytest

from repositories.product_repository import ProductRepository
from schemas import ProductAddDTO, ProductDTO
from services.product_service import ProductService

product_data = ProductAddDTO(
    title="example",
    price=1000,
    stock_qty=10,
)


class TestProductService:
    @pytest.mark.asyncio
    async def test_create_product(self):
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

        product_service = ProductService(product_repo=mock_product_repo)
        result = await product_service.create(product_data)

        # проверка что для асинхронного метода create() был всего 1 await и с указанным объектом
        mock_product_repo.create.assert_awaited_once_with(product_data)
        mock_product_repo.session.commit.assert_awaited_once()
        assert isinstance(result, ProductDTO)
        assert result.title == "example"

    @pytest.mark.asyncio
    async def test_delete_product(self):
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_product_repo.session = Mock()
        mock_product_repo.session.commit = AsyncMock()
        mock_product_repo.session.rollback = AsyncMock()

        product_id = 1

        fake_product = Mock(id=product_id, title="example", price=1000, stock_qty=10)
        mock_product_repo.get_by_id.return_value = fake_product

        mock_product_repo.delete.return_value = None

        product_service = ProductService(product_repo=mock_product_repo)
        result = await product_service.delete(product_id)

        assert result is None

        mock_product_repo.get_by_id.assert_awaited_once_with(product_id)
        mock_product_repo.delete.assert_awaited_once_with(fake_product)
        mock_product_repo.session.commit.assert_awaited_once()

        # rollback не должен быть вызван
        mock_product_repo.session.rollback.assert_not_called()
