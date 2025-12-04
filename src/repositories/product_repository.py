from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Product
from schemas import ProductAddDTO, ProductUpdateDTO


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        return await self.session.get(Product, product_id)

    async def create(self, product_data: ProductAddDTO) -> Product:
        product = Product(**product_data.model_dump())
        self.session.add(product)

        await self.session.flush()
        await self.session.refresh(product)

        return product

    async def delete(self, product: Product) -> None:
        await self.session.delete(product)
        await self.session.flush()

    async def update(self, product: Product, product_data: ProductUpdateDTO) -> Product:
        update_data = product_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)

        await self.session.flush()
        await self.session.refresh(product)

        return product
    
    async def get_all(self) -> list[Product]:
        stmt = select(Product)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_title(self, title: str) -> Optional[Product]:
        stmt = select(Product).where(Product.title == title)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
