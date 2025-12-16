from src.messaging.broker import broker
from src.messaging.constants import Events
from src.schemas import CartDTO


class CartProducer:
    @staticmethod
    async def created(cart: CartDTO):
        await broker.publish(
            message=cart,
            routing_key=Events.CART_CREATED,
        )

    @staticmethod
    async def updated(cart: CartDTO):
        await broker.publish(
            message=cart,
            routing_key=Events.CART_UPDATED,
        )

    @staticmethod
    async def deleted(cart: CartDTO):
        await broker.publish(message=cart, routing_key=Events.CART_DELETED)
