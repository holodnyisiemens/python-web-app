from src.messaging.broker import broker
from src.messaging.constants import Events


class ProductProducer:
    @staticmethod
    async def created(product: dict):
        await broker.publish(
            message=product,
            routing_key=Events.PRODUCT_CREATED,
        )

    @staticmethod
    async def updated(product: dict):
        await broker.publish(
            message=product,
            routing_key=Events.PRODUCT_UPDATED,
        )

    @staticmethod
    async def deleted(product: dict):
        await broker.publish(message=product, routing_key=Events.PRODUCT_DELETED)
