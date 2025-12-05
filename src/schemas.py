from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )


class UserAddDTO(BaseDTO):
    username: str
    email: EmailStr
    description: Optional[str] = None


class UserDTO(UserAddDTO):
    id: UUID


class UserUpdateDTO(BaseDTO):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    description: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        # ValidationError for extra attributes
        extra="forbid",
    )


class UserRelDTO(UserDTO):
    addresses: list["AddressDTO"]


class AddressAddDTO(BaseDTO):
    user_id: UUID
    street: str
    city: str
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: str
    is_primary: bool = False


class AddressDTO(AddressAddDTO):
    id: UUID


class AddressUpdateDTO(BaseDTO):
    user_id: Optional[UUID] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    is_primary: Optional[bool] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        # ValidationError for extra attributes
        extra="forbid",
    )


class AddressRelDTO(AddressDTO):
    user: "UserDTO"


class ProductAddDTO(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    stock_qty: int


class ProductDTO(ProductAddDTO):
    id: UUID


class ProductUpdateDTO(BaseDTO):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_qty: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        # ValidationError for extra attributes
        extra="forbid",
    )


class ProductRelDTO(ProductDTO):
    carts: list["CartDTO"]


class CartAddDTO(BaseDTO):
    customer_id: UUID
    delivery_address_id: UUID


class CartDTO(CartAddDTO):
    id: UUID


class CartUpdateDTO(BaseDTO):
    customer_id: Optional[UUID] = None
    delivery_address_id: Optional[UUID] = None

    model_config = ConfigDict(
        from_attributes=True,
        # ValidationError for extra attributes
        extra="forbid",
    )


class CartRelDTO(CartDTO):
    products: list["ProductDTO"]


class CartProductAddDTO(BaseDTO):
    cart_id: UUID
    product_id: UUID
    quantity: int = 1


class CartProductDTO(CartProductAddDTO):
    pass
