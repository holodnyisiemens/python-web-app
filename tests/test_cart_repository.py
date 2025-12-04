import pytest

from schemas import CartAddDTO, CartUpdateDTO, CartDTO, AddressAddDTO, UserAddDTO, UserDTO, AddressDTO
from repositories.cart_repository import CartRepository
from repositories.user_repository import UserRepository
from repositories.address_repository import AddressRepository


user_data_1 = UserAddDTO(
    username="Alexey",
    email="email@example.com",
)

user_data_2 = UserAddDTO(
    username="Alexander",
    email="another@example.com",
)


class TestCartRepository:
    async def _create_test_user_and_address(self, user_repository: UserRepository, address_repository: AddressRepository, user_data: UserAddDTO) -> tuple[UserDTO, AddressDTO]:
        user = await user_repository.create(user_data)

        address_data = AddressAddDTO(
            user_id=user.id,
            street="Lenina",
            city="Ekb",
            country="Russia",
        )
        address = await address_repository.create(address_data)

        return user, address

    async def _create_test_cart(self, cart_repository: CartRepository, user_repository: UserRepository, address_repository: AddressRepository) -> tuple[CartDTO, CartAddDTO]:
        user, address = await self._create_test_user_and_address(user_repository, address_repository, user_data_1)

        cart_data = CartAddDTO(
            customer_id=user.id,
            delivery_address_id=address.id,
        )

        return await cart_repository.create(cart_data), cart_data

    @pytest.mark.asyncio
    async def test_create_cart(self, cart_repository: CartRepository, user_repository: UserRepository, address_repository: AddressRepository):
        cart, cart_data = await self._create_test_cart(cart_repository, user_repository, address_repository)

        assert cart.id is not None
        assert cart.customer_id == cart_data.customer_id
        assert cart.delivery_address_id == cart_data.delivery_address_id

    @pytest.mark.asyncio
    async def test_update_cart(self, cart_repository: CartRepository, user_repository: UserRepository, address_repository: AddressRepository):
        cart, _ = await self._create_test_cart(cart_repository, user_repository, address_repository)
        new_user, new_address = await self._create_test_user_and_address(user_repository, address_repository, user_data_2)

        new_cart_data = CartUpdateDTO(customer_id=new_user.id, delivery_address_id=new_address.id)

        await cart_repository.update(cart.id, new_cart_data)

        updated_cart = await cart_repository.get_by_id(cart.id)
        
        assert updated_cart.id == cart.id
        assert updated_cart.customer_id == new_user.id
        assert updated_cart.delivery_address_id == new_address.id

    @pytest.mark.asyncio
    async def test_delete_cart(self, cart_repository: CartRepository, user_repository: UserRepository, address_repository: AddressRepository):
        cart, _ = await self._create_test_cart(cart_repository, user_repository, address_repository)
        await cart_repository.delete(cart.id)

        found_cart = await cart_repository.get_by_id(cart.id)
        assert found_cart is None
