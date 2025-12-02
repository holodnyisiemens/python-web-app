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


class AddressRelDTO(AddressDTO):
    user: "UserDTO"


class ProductAddDTO(BaseModel):
    title: str
    description: Optional[str] = None
    price: float


class ProductDTO(ProductAddDTO):
    id: UUID


class ProductUpdateDTO(BaseDTO):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

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


class CartRelDTO(CartDTO):
    products: list["ProductDTO"]


class CartProductAddDTO(BaseDTO):
    cart_id: UUID
    product_id: UUID
    quantity: int = 1


class CartProductDTO(CartProductAddDTO):
    pass
