import asyncio
import time

from src.database import async_session_factory
from src.messaging.broker import broker
from src.messaging.producers.product import ProductProducer
from src.repositories.product_repository import ProductRepository
from src.schemas import ProductAddDTO
from src.services.product_service import ProductService


async def create_products(product_service: ProductService):
    # 5 продуктов для создания
    products = [
        ProductAddDTO(
            title=f"JBL_{i}",
            price=1500,
            stock_qty=10,
        )
        for i in range(1, 6)
    ]

    for p in products:
        await product_service.create(p)
        await ProductProducer.created(p)


async def main():
    async with async_session_factory() as session:
        await broker.connect()

        product_repo = ProductRepository(session)
        product_service = ProductService(product_repo)
        await create_products(product_service)

        time.sleep(30)

        await broker.stop()


if __name__ == "__main__":
    asyncio.run(main())
