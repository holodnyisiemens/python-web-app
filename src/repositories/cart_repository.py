from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Cart, Product, CartProduct
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

    async def delete(self, cart: Cart) -> None:
        await self.session.delete(cart)
        await self.session.flush()

    async def update(self, cart: Cart, cart_data: CartUpdateDTO) -> Cart:
        # обновляем только переданные поля
        update_data = cart_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(cart, field, value)

        await self.session.flush()
        await self.session.refresh(cart)

        return cart
    
    async def get_cart_with_items(self, cart: Cart) -> Cart:
        stmt = (
            select(Cart)
            .where(Cart.id == cart.id)
            .options(selectinload(Cart.cart_items))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_product(self, cart: Cart, product: Product, qty: int = 1) -> CartProduct:
        # ищем, есть ли уже запись в cart_product
        cart = await self.get_cart_with_items(cart)

        for item in cart.cart_items:
            if item.product_id == product.id:
                item.quantity += qty
                await self.session.flush()
                return item
        
        new_item = CartProduct(
            cart_id=cart.id,
            product_id=product.id,
            quantity=qty,
        )

        cart.cart_items.append(new_item)
        
        self.session.add(new_item)
        await self.session.flush()
        return new_item
