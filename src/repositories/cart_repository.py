from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Cart
from schemas import CartAddDTO, CartUpdateDTO


class CartRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, cart_id: UUID) -> Optional[Cart]:
        return await self.session.get(Cart, cart_id)

    async def create(self, cart_data: CartAddDTO) -> Cart:
        cart = Cart(**cart_data.model_dump())
        self.session.add(cart)

        await self.session.flush()
        await self.session.refresh(cart)
        
        return cart

    async def delete(self, cart_id: UUID) -> Optional[Cart]:
        stmt = select(Cart).where(Cart.id == cart_id)
        result = await self.session.execute(stmt)
        cart = result.scalar_one_or_none()
        if not cart:
            return None
        await self.session.delete(cart)
        await self.session.commit()
        return cart

    async def update(self, cart_id: UUID, cart_data: CartUpdateDTO) -> Cart:
        stmt = select(Cart).where(Cart.id == cart_id)
        result = await self.session.execute(stmt)
        cart = result.scalar_one_or_none()
        if not cart:
            return None
        # обновляем только переданные поля
        update_data = cart_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(cart, field, value)

        await self.session.commit()
        await self.session.refresh(cart)
        return cart
