from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )


class UserAddDTO(BaseDTO):
    username: str
    email: EmailStr
    description: Optional[str] = None


class UserDTO(UserAddDTO):
    id: int


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
    user_id: int
    street: str
    city: str
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: str
    is_primary: bool = False


class AddressDTO(AddressAddDTO):
    id: int


class AddressUpdateDTO(BaseDTO):
    user_id: Optional[int] = None
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


class ProductAddDTO(BaseDTO):
    title: str
    description: Optional[str] = None
    price: float
    stock_qty: int


class ProductDTO(ProductAddDTO):
    id: int


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
    customer_id: int
    delivery_address_id: int


class CartDTO(CartAddDTO):
    id: int
    total_amount: float


class CartUpdateDTO(BaseDTO):
    customer_id: Optional[int] = None
    delivery_address_id: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        # ValidationError for extra attributes
        extra="forbid",
    )


class CartRelDTO(CartDTO):
    products: list["ProductDTO"]
    cart_items: list["CartProductDTO"]


class CartProductAddDTO(BaseDTO):
    cart_id: int
    product_id: int
    quantity: int = 1


class CartProductDTO(CartProductAddDTO):
    pass


class CartProductRelDTO(CartProductDTO):
    cart: CartDTO
    product: ProductDTO


class ReportAddDTO(BaseDTO):
    order_id: int
    count_product: int


class ReportDTO(ReportAddDTO):
    report_at: datetime
