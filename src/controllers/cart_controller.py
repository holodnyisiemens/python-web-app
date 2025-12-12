from litestar import Controller, delete, get, post, put

from schemas import (
    CartAddDTO,
    CartDTO,
    CartProductAddDTO,
    CartProductDTO,
    CartUpdateDTO,
)
from services.cart_service import CartService


class CartController(Controller):
    path = "/carts"

    @get("/{cart_id:int}")
    async def get_cart_by_id(self, cart_service: CartService, cart_id: int) -> CartDTO:
        """Получить заказ по ID"""
        return await cart_service.get_by_id(cart_id)

    @post()
    async def create_cart(self, cart_service: CartService, data: CartAddDTO) -> CartDTO:
        """Создать новый заказ"""
        return await cart_service.create(data)

    @delete("/{cart_id:int}")
    async def delete_cart(self, cart_service: CartService, cart_id: int) -> None:
        """Удаление заказа"""
        return await cart_service.delete(cart_id)

    @put("/{cart_id:int}")
    async def update_cart(
        self, cart_service: CartService, cart_id: int, data: CartUpdateDTO
    ) -> CartDTO:
        """Обновление параметров заказа"""
        return await cart_service.update(cart_id, data)

    @get("/")
    async def get_all_carts(self, cart_service: CartService) -> list[CartDTO]:
        """Получить всех пользователей"""
        return await cart_service.get_all()

    @post("/{cart_id:int}/items")
    async def add_product_to_cart(
        self,
        cart_service: CartService,
        cart_id: int,
        data: CartProductAddDTO,
    ) -> CartProductDTO:
        """Добавить товар в корзину"""
        return await cart_service.add_product(
            cart_id=cart_id,
            product_id=data.product_id,
            qty=data.quantity,
        )
