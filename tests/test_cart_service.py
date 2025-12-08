import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from schemas import CartAddDTO, CartDTO
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository
from repositories.address_repository import AddressRepository
from services.cart_service import CartService


class TestCartService:
    @pytest.mark.asyncio
    async def test_create_cart(self, cart_data_1: CartDTO):
        # мокаем репозиторий и объекты в нем
        mock_cart_repo = AsyncMock(spec=CartRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_address_repo = AsyncMock(spec=AddressRepository)

        mock_cart_repo.session = Mock()
        mock_cart_repo.session.commit = AsyncMock()
        mock_cart_repo.session.rollback = AsyncMock()

        # то, что вернёт create()
        mock_cart_repo.create.return_value = CartDTO(
            id=uuid4(),
            customer_id=cart_data_1.customer_id,
            delivery_address_id=cart_data_1.delivery_address_id,
        )

        cart_service = CartService(
            cart_repo=mock_cart_repo,
            user_repo=mock_user_repo,
            address_repo=mock_address_repo,
        )
        
        result = await cart_service.create(cart_data_1)

        # проверка что для асинхронного метода create() был всего 1 await и с указанным объектом
        mock_cart_repo.create.assert_awaited_once_with(cart_data_1)
        mock_cart_repo.session.commit.assert_awaited_once()
        assert isinstance(result, CartDTO)
        assert result.customer_id == cart_data_1.customer_id

    @pytest.mark.asyncio
    async def test_delete_cart(self, cart_data_1: CartDTO):
        mock_cart_repo = AsyncMock(spec=CartRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_address_repo = AsyncMock(spec=AddressRepository)

        mock_cart_repo.session = Mock()
        mock_cart_repo.session.commit = AsyncMock()
        mock_cart_repo.session.rollback = AsyncMock()

        cart_id = uuid4()

        fake_cart = Mock(
            id=cart_id,
            customer_id=cart_data_1.customer_id,
            delivery_address_id=cart_data_1.delivery_address_id,
        )

        mock_cart_repo.get_by_id.return_value = fake_cart

        mock_cart_repo.delete.return_value = None

        cart_service = CartService(cart_repo=mock_cart_repo, user_repo=mock_user_repo, address_repo=mock_address_repo)
        result = await cart_service.delete(cart_id)

        assert result is None

        mock_cart_repo.get_by_id.assert_awaited_once_with(cart_id)
        mock_cart_repo.delete.assert_awaited_once_with(fake_cart)
        mock_cart_repo.session.commit.assert_awaited_once()

        # rollback не должен быть вызван
        mock_cart_repo.session.rollback.assert_not_called()
