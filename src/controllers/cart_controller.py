from litestar import Controller, get, post, put, delete
from litestar.status_codes import HTTP_200_OK

from schemas import CartDTO, CartAddDTO, CartUpdateDTO
from services.cart_service import CartService


class CartController(Controller):
    path = "/carts"
    
    @get("/{cart_id:int}", status_code=HTTP_200_OK)
    async def get_cart_by_id(self, cart_service: CartService, cart_id: int) -> CartDTO:
        """Получить заказ по ID""" 
        return await cart_service.get_by_id(cart_id)

    @post()
    async def create_cart(self, cart_service: CartService, data: CartAddDTO) -> CartDTO:
        """Создать новый заказ"""
        return await cart_service.create(data)

    @delete("/{cart_id:int}", status_code=HTTP_200_OK)
    async def delete_cart(self, cart_service: CartService, cart_id: int) -> None:
        """Удаление заказа"""
        return await cart_service.delete(cart_id)

    @put("/{cart_id:int}")
    async def update_cart(self, cart_service: CartService, cart_id: int, data: CartUpdateDTO) -> CartDTO:
        """Обновление параметров заказа"""
        return await cart_service.update(cart_id, data)

    @get("/")
    async def get_all_carts(self, cart_service: CartService) -> list[CartDTO]:
        """Получить всех пользователей"""
        return await cart_service.get_all()
