from src.messaging.broker import broker
from src.messaging.constants import Events
from src.schemas import CartDTO


@broker.subscriber(Events.CART_CREATED)
async def on_cart_created(cart: CartDTO):
    print(f"Created cart with ID: {cart.id}")


@broker.subscriber(Events.CART_UPDATED)
async def on_cart_updated(cart: CartDTO):
    print(f"Updated cart with ID: {cart.id}")


@broker.subscriber(Events.CART_DELETED)
async def on_cart_deleted(cart: CartDTO):
    print(f"Deleted cart with ID: {cart.id}")
