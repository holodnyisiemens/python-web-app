from uuid import UUID

from litestar.exceptions import NotFoundException, HTTPException

from repositories.cart_repository import CartRepository
from repositories.user_repository import UserRepository
from repositories.address_repository import AddressRepository
from schemas import CartDTO, CartAddDTO, CartUpdateDTO


class CartService:
    def __init__(self, cart_repo: CartRepository, user_repo: UserRepository, address_repo: AddressRepository):
        self.cart_repo = cart_repo
        self.user_repo = user_repo
        self.address_repo = address_repo

    async def get_by_id(self, cart_id: UUID) -> CartDTO:
        cart = await self.cart_repo.get_by_id(cart_id)
        if not cart:
            raise NotFoundException(detail=f"Cart with ID {cart_id} not found")
        return CartDTO.model_validate(cart)

    async def create(self, cart_data: CartAddDTO) -> CartDTO:
        try:
            cart = await self.cart_repo.create(cart_data)
            await self.cart_repo.session.commit()
        except:
            await self.cart_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"Cart create error")
    
        return CartDTO.model_validate(cart)

    async def delete(self, cart_id: UUID) -> None:
        cart = await self.cart_repo.get_by_id(cart_id)
        if not cart:
            raise NotFoundException(detail=f"Cart with ID {cart_id} not found")

        try:
            await self.cart_repo.delete(cart)
            await self.cart_repo.session.commit()
        except:
            await self.cart_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"Cart delete error")

    async def update(self, cart_id: UUID, cart_data: CartUpdateDTO) -> CartDTO:
        cart = await self.cart_repo.get_by_id(cart_id)
        if not cart:
            raise NotFoundException(detail=f"Cart with ID {cart_id} not found")

        if cart_data.customer_id is not None:
            customer = await self.user_repo.get_by_id(cart_data.customer_id)
            if not customer:
                raise HTTPException(status_code=404, detail=f"User with ID {cart_data.customer_id} not found")

        if cart_data.delivery_address_id is not None:
            delivery_address = await self.address_repo.get_by_id(cart_data.delivery_address_id)
            if not delivery_address:
                raise HTTPException(status_code=404, detail=f"Address with ID {cart_data.delivery_address_id} not found")

        try:
            await self.cart_repo.update(cart, cart_data)
            await self.cart_repo.session.commit()
        except:
            await self.cart_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"Cart update error")    

        return CartDTO.model_validate(cart)
