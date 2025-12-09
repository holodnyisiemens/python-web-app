import pytest

from schemas import CartAddDTO, CartUpdateDTO, CartDTO, UserDTO, ProductDTO
from repositories.cart_repository import CartRepository


class TestCartRepository:
    @pytest.mark.asyncio
    async def test_create_cart(self, cart_repository: CartRepository, cart_data_1: CartAddDTO):
        cart = await cart_repository.create(cart_data_1)

        assert cart.id is not None
        assert cart.customer_id == cart_data_1.customer_id
        assert cart.delivery_address_id == cart_data_1.delivery_address_id

    @pytest.mark.asyncio
    async def test_update_cart(self, cart_repository: CartRepository, cart_1: CartDTO, user_2: UserDTO, address_2: UserDTO):
        new_cart_data = CartUpdateDTO(customer_id=user_2.id, delivery_address_id=address_2.id)

        await cart_repository.update(cart_1, new_cart_data)

        updated_cart = await cart_repository.get_by_id(cart_1.id)
        
        assert updated_cart.id == cart_1.id
        assert updated_cart.customer_id == user_2.id
        assert updated_cart.delivery_address_id == address_2.id

    @pytest.mark.asyncio
    async def test_delete_cart(self, cart_repository: CartRepository, cart_1: CartDTO):
        await cart_repository.delete(cart_1)

        found_cart = await cart_repository.get_by_id(cart_1.id)
        assert found_cart is None

    @pytest.mark.asyncio
    async def test_add_product(self, cart_repository: CartRepository, cart_1: CartDTO, product_1: ProductDTO):
        cart_item = await cart_repository.add_product(cart_1, product_1, qty=2)
        cart = await cart_repository.get_by_id(cart_1.id)

        assert cart_item.cart_id == cart_1.id
        assert cart_item.product_id == product_1.id
        assert cart_item.quantity == 2
        assert cart.total_amount == product_1.price * cart_item.quantity

    @pytest.mark.asyncio
    async def test_add_same_product_multiple_times(self, cart_repository: CartRepository, cart_1: CartDTO, product_1: ProductDTO):
        # добавляем продукт первый раз
        cart_item_1 = await cart_repository.add_product(cart_1, product_1, qty=2)
        cart = await cart_repository.get_by_id(cart_1.id)

        assert cart_item_1.quantity == 2

        # добавляем тот же продукт ещё раз
        cart_item_2 = await cart_repository.add_product(cart_1, product_1, qty=3)
        assert cart_item_2.cart_id == cart_1.id
        assert cart_item_2.product_id == product_1.id

        assert cart_item_2.quantity == 5
        assert cart_item_1 == cart_item_2
        assert cart.total_amount == 5 * product_1.price

    @pytest.mark.asyncio
    async def test_get_all_carts(self, cart_repository: CartRepository, cart_1: CartDTO, cart_2: CartDTO):
        cart_list = await cart_repository.get_all()

        cart_customers = [cart.customer_id for cart in cart_list]

        assert len(cart_list) == 2
        assert cart_customers[0] == cart_1.customer_id
        assert cart_customers[1] == cart_2.customer_id
