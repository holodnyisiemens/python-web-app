import pytest

from schemas import CartAddDTO, CartUpdateDTO, CartDTO, AddressAddDTO, UserAddDTO, UserDTO, AddressDTO, ProductAddDTO, ProductDTO
from repositories.cart_repository import CartRepository
from repositories.user_repository import UserRepository
from repositories.address_repository import AddressRepository
from repositories.product_repository import ProductRepository


user_data_1 = UserAddDTO(
    username="Alexey",
    email="email@example.com",
)

user_data_2 = UserAddDTO(
    username="Alexander",
    email="another@example.com",
)

product_data_1 = ProductAddDTO(
    title="Headphones",
    price=999.99,
    stock_qty=2,
)

product_data_2 = ProductAddDTO(
    title="JBL",
    price=7000,
    stock_qty=0,
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
        cart = await cart_repository.create(cart_data)
        return cart, cart_data

    async def _create_test_product(self, product_repository: ProductRepository, product_data: ProductAddDTO) -> tuple[ProductDTO, ProductAddDTO]:
        product = await product_repository.create(product_data)
        return product, product_data

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

        await cart_repository.update(cart, new_cart_data)

        updated_cart = await cart_repository.get_by_id(cart.id)
        
        assert updated_cart.id == cart.id
        assert updated_cart.customer_id == new_user.id
        assert updated_cart.delivery_address_id == new_address.id

    @pytest.mark.asyncio
    async def test_delete_cart(self, cart_repository: CartRepository, user_repository: UserRepository, address_repository: AddressRepository):
        cart, _ = await self._create_test_cart(cart_repository, user_repository, address_repository)
        await cart_repository.delete(cart)

        found_cart = await cart_repository.get_by_id(cart.id)
        assert found_cart is None

    @pytest.mark.asyncio
    async def test_add_product(self, cart_repository: CartRepository, user_repository: UserRepository, address_repository: AddressRepository, product_repository: ProductRepository):
        cart, _ = await self._create_test_cart(cart_repository, user_repository, address_repository)
        product, _ = await self._create_test_product(product_repository, product_data_1)

        cart_item = await cart_repository.add_product(cart, product, qty=2)

        assert cart_item.product_id == product.id
        assert cart_item.cart_id == cart.id
        assert cart_item.quantity == 2

    @pytest.mark.asyncio
    async def test_add_same_product_multiple_times(self, cart_repository: CartRepository, user_repository: UserRepository, address_repository: AddressRepository, product_repository: ProductRepository):
        cart, _ = await self._create_test_cart(cart_repository, user_repository, address_repository)
        product, _ = await self._create_test_product(product_repository, product_data_1)

        # добавляем продукт первый раз
        cart_item_1 = await cart_repository.add_product(cart, product, qty=2)
        assert cart_item_1.quantity == 2

        # добавляем тот же продукт ещё раз
        cart_item_2 = await cart_repository.add_product(cart, product, qty=3)
        assert cart_item_2.product_id == product.id
        assert cart_item_2.cart_id == cart.id

        assert cart_item_2.quantity == 5
        assert cart_item_1 is cart_item_2
