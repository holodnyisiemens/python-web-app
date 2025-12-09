from litestar.exceptions import NotFoundException, HTTPException

from repositories.cart_repository import CartRepository
from repositories.user_repository import UserRepository
from repositories.address_repository import AddressRepository
from repositories.product_repository import ProductRepository
from schemas import CartDTO, CartAddDTO, CartUpdateDTO, CartProductDTO


class CartService:  
    def __init__(self, cart_repo: CartRepository, user_repo: UserRepository, address_repo: AddressRepository, product_repo: ProductRepository):
        self.cart_repo = cart_repo
        self.user_repo = user_repo
        self.address_repo = address_repo
        self.product_repo = product_repo

    async def get_by_id(self, cart_id: int) -> CartDTO:
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

    async def delete(self, cart_id: int) -> None:
        cart = await self.cart_repo.get_by_id(cart_id)
        if not cart:
            raise NotFoundException(detail=f"Cart with ID {cart_id} not found")

        try:
            await self.cart_repo.delete(cart)
            await self.cart_repo.session.commit()
        except:
            await self.cart_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"Cart delete error")

    async def update(self, cart_id: int, cart_data: CartUpdateDTO) -> CartDTO:
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
    
    async def add_product(self, cart_id: int, product_id: int, qty: int = 1) -> CartProductDTO:
        cart = await self.cart_repo.get_by_id(cart_id)
        if not cart:
            raise HTTPException(status_code=404, detail=f"Cart with ID {cart_id} not found")

        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

        try:
            cart = await self.cart_repo.get_cart_with_items(cart)
            await self.cart_repo.add_product(cart, product, qty)
            await self.cart_repo.session.commit()
        except:
            await self.cart_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"Error while add product to cart") 

    async def get_all(self) -> list[CartDTO]:
        return await self.cart_repo.get_all()
    