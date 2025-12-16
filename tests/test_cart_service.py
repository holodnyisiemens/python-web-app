from unittest.mock import AsyncMock, Mock

import pytest

from src.repositories.address_repository import AddressRepository
from src.repositories.cart_repository import CartRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.user_repository import UserRepository
from src.schemas import CartAddDTO, CartDTO, ProductDTO
from src.services.cart_service import CartService


class TestCartService:
    @pytest.mark.asyncio
    async def test_create_cart_success(
        self, cart_data_1: CartAddDTO, product_1: ProductDTO, product_2: ProductDTO
    ):
        # мокаем репозиторий и объекты в нем
        mock_cart_repo = AsyncMock(spec=CartRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_address_repo = AsyncMock(spec=AddressRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)

        mock_cart_repo.session = Mock()
        mock_cart_repo.session.commit = AsyncMock()
        mock_cart_repo.session.rollback = AsyncMock()

        mock_cart = Mock(
            id=1,
            customer_id=cart_data_1.customer_id,
            delivery_address_id=cart_data_1.delivery_address_id,
            total_amount=0.0,
        )

        mock_cart_repo.create = AsyncMock(return_value=mock_cart)
        mock_cart_repo.get_cart_with_items = AsyncMock(return_value=mock_cart)

        cart_service = CartService(
            cart_repo=mock_cart_repo,
            user_repo=mock_user_repo,
            address_repo=mock_address_repo,
            product_repo=mock_product_repo,
        )

        cart_dto = await cart_service.create(cart_data_1)
        # проверка, что для асинхронного метода create() был всего 1 await и с указанным объектом
        mock_cart_repo.create.assert_awaited_once_with(cart_data_1)
        # проверка, что коммит был вызван 1 раз
        mock_cart_repo.session.commit.assert_awaited_once()

        await cart_service.add_product(cart_dto.id, product_1.id)
        await cart_service.add_product(cart_dto.id, product_2.id, qty=2)

        assert isinstance(cart_dto, CartDTO)
        assert cart_dto.customer_id == cart_data_1.customer_id
        assert cart_dto.delivery_address_id == cart_data_1.delivery_address_id

    @pytest.mark.asyncio
    async def test_delete_cart(self, cart_data_1: CartDTO):
        mock_cart_repo = AsyncMock(spec=CartRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_address_repo = AsyncMock(spec=AddressRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)

        mock_cart_repo.session = Mock()
        mock_cart_repo.session.commit = AsyncMock()
        mock_cart_repo.session.rollback = AsyncMock()

        cart_id = 1

        fake_cart = Mock(
            id=cart_id,
            customer_id=cart_data_1.customer_id,
            delivery_address_id=cart_data_1.delivery_address_id,
        )

        mock_cart_repo.get_by_id.return_value = fake_cart

        mock_cart_repo.delete.return_value = None

        cart_service = CartService(
            cart_repo=mock_cart_repo,
            user_repo=mock_user_repo,
            address_repo=mock_address_repo,
            product_repo=mock_product_repo,
        )

        result = await cart_service.delete(cart_id)

        assert result is None

        mock_cart_repo.get_by_id.assert_awaited_once_with(cart_id)
        mock_cart_repo.delete.assert_awaited_once_with(fake_cart)
        mock_cart_repo.session.commit.assert_awaited_once()

        # rollback не должен быть вызван
        mock_cart_repo.session.rollback.assert_not_called()
