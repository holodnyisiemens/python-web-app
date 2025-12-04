import pytest

from schemas import CartAddDTO, CartUpdateDTO, CartDTO, AddressAddDTO, UserAddDTO, UserDTO, AddressDTO
from repositories.cart_repository import CartRepository
from repositories.user_repository import UserRepository
from repositories.address_repository import AddressRepository


class TestCartRepository:
    async def _create_test_cart(self, cart_repository: CartRepository, cart_data: CartAddDTO) -> CartDTO:
        return await cart_repository.create(cart_data)

    async def _create_test_user(self, user_repository: UserRepository, user_data: UserAddDTO) -> UserDTO:
        return await user_repository.create(user_data)

    async def _create_test_address(self, address_repository: AddressRepository, address_data: AddressAddDTO) -> AddressDTO:
        return await address_repository.create(address_data)

    @pytest.mark.asyncio
    async def test_create_cart(self, cart_repository: CartRepository, user_repository: UserRepository, address_repository: AddressRepository):
        user_data = UserAddDTO(
            username="Alexey",
            email="email@example.com",
        )
        user = await self._create_test_user(user_repository, user_data)

        address_data = AddressAddDTO(
            user_id=user.id,
            street="Lenina",
            city="Ekb",
            country="Russia",
        )
        address = await self._create_test_address(address_repository, address_data)

        cart_data = CartAddDTO(
            customer_id=user.id,
            delivery_address_id=address.id,
        )
        cart = await self._create_test_cart(cart_repository, cart_data)

        assert cart.id is not None
        assert cart.customer_id == cart_data.customer_id
        assert cart.delivery_address_id == cart_data.delivery_address_id

    # @pytest.mark.asyncio
    # async def test_update_cart(self, cart_repository: CartRepository):
    #     cart = await self._create_test_cart(cart_repository, cart_data)

    #     new_customer_id = uuid4()
    #     new_cart_data = CartUpdateDTO(customer_id=new_customer_id)

    #     await cart_repository.update(cart.id, new_cart_data)

    #     updated_cart = await cart_repository.get_by_id(cart.id)
        
    #     assert updated_cart.customer_id == new_customer_id

    #     assert updated_cart.id == cart.id
    #     assert updated_cart.delivery_address_id == cart.delivery_address_id

    # @pytest.mark.asyncio
    # async def test_delete_cart(self, cart_repository: CartRepository):
    #     cart = await self._create_test_cart(cart_repository, cart_data)
    #     await cart_repository.delete(cart.id)

    #     found_cart = await cart_repository.get_by_id(cart.id)
    #     assert found_cart is None
