import pytest

from litestar.status_codes import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_400_BAD_REQUEST

from schemas import CartDTO, CartAddDTO, UserDTO, AddressDTO, CartProductDTO


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

    @pytest.mark.asyncio
    async def test_create_cart(self, client, mock_cart_service, cart_data_1: CartAddDTO):
        cart_id = 1
        expected_cart = CartDTO(
            id=cart_id,
            customer_id=cart_data_1.customer_id,
            delivery_address_id=cart_data_1.delivery_address_id,
            total_amount=0.0,
        )

        mock_cart_service.create.return_value = expected_cart

        response = await client.post("/carts", json=cart_data_1.model_dump())

        assert response.status_code == HTTP_201_CREATED
        data = response.json()

        assert data["id"] == cart_id
        assert data["customer_id"] == cart_data_1.customer_id
        assert data["delivery_address_id"] == cart_data_1.delivery_address_id

        mock_cart_service.create.assert_awaited_once_with(cart_data_1)

    @pytest.mark.asyncio
    async def test_delete_cart_failed(self, client, mock_cart_service):
        cart_id = 5
        mock_cart_service.delete.return_value = None
        response = await client.delete(f"/carts/{cart_id}")

        assert response.status_code == HTTP_204_NO_CONTENT
        mock_cart_service.delete.assert_awaited_once_with(cart_id)

    @pytest.mark.asyncio
    async def test_update_cart(self, client, mock_cart_service, user_2: UserDTO, address_2: AddressDTO):
        cart_id = 3
        update_data = {
            "customer_id": user_2.id,
            "delivery_address_id": address_2.id,
        }

        expected_updated = {
            "id": cart_id,
            "customer_id": user_2.id,
            "delivery_address_id": address_2.id,
            "total_amount": 0.0,
        }

        mock_cart_service.update.return_value = expected_updated

        response = await client.put(f"/carts/{cart_id}", json=update_data)

        assert response.status_code == HTTP_200_OK
        data = response.json()

        assert data["customer_id"] == user_2.id
        assert data["delivery_address_id"] == address_2.id

    @pytest.mark.asyncio
    async def test_get_all_carts(self, client, mock_cart_service):
        mock_cart_service.get_all.return_value = [
            {
                "id": 1,
                "customer_id": 10,
                "delivery_address_id": 20,
                "total_amount": 100.0,
            },
            {
                "id": 2,
                "customer_id": 11,
                "delivery_address_id": 21,
                "total_amount": 200.0,
            },
        ]

        response = await client.get("/carts/")

        assert response.status_code == HTTP_200_OK
        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[1]["total_amount"] == 200.0

        mock_cart_service.get_all.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_add_product_to_cart_success(
        self,
        client,
        mock_cart_service,
    ):
        cart_id = 1
        product_id = 42
        quantity = 3

        payload = {
            "cart_id": cart_id,
            "product_id": product_id,
            "quantity": quantity,
        }

        expected_item = CartProductDTO(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
        )

        mock_cart_service.add_product.return_value = expected_item

        response = await client.post(f"/carts/{cart_id}/items", json=payload)

        assert response.status_code == HTTP_201_CREATED
        data = response.json()

        assert data["cart_id"] == cart_id
        assert data["product_id"] == product_id
        assert data["quantity"] == quantity
