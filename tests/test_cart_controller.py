import pytest

from schemas import CartDTO, CartAddDTO


class TestCartController:
    @pytest.mark.asyncio
    async def test_get_cart_by_id(self, mock_cart_service, client, cart_data_1: CartAddDTO):        
        cart_id = 1
        expected_cart = CartDTO(
            id=cart_id,
            customer_id=cart_data_1.customer_id,
            delivery_address_id=cart_data_1.delivery_address_id,
            total_amount=0.0,
        )

        mock_cart_service.get_by_id.return_value = expected_cart

        response = await client.get(f"/carts/{cart_id}")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == cart_id
        assert data["customer_id"] == cart_data_1.customer_id
        assert data["delivery_address_id"] == cart_data_1.delivery_address_id

        mock_cart_service.get_by_id.assert_awaited_once_with(cart_id)
