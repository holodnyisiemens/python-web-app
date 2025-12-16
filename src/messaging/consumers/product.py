from src.messaging.broker import broker
from src.messaging.constants import Events
from src.schemas import ProductDTO


@broker.subscriber(Events.PRODUCT_CREATED)
async def on_product_created(product: ProductDTO):
    print(f"Created product with ID: {product.id}")


@broker.subscriber(Events.PRODUCT_UPDATED)
async def on_product_updated(product: ProductDTO):
    print(f"Updated product with ID: {product.id}")


@broker.subscriber(Events.PRODUCT_DELETED)
async def on_product_deleted(product: ProductDTO):
    print(f"Deleted product with ID: {product.id}")
