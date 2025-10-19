from orm import ORM
from schemas import UserAddDTO, AddressAddDTO, UserRelDTO, ProductAddDTO, CartAddDTO, CartProductAddDTO, CartRelDTO


user_1 = ORM.insert_user(
    UserAddDTO(
        username="John Doe",
        email="jdoe@example.com",
    )
)

address_1 = ORM.insert_address(
    AddressAddDTO(
        user_id=user_1.id,
        street="221B Baker Street",
        city="London",
        state="Greater London",
        zip_code="NW1 6XE",
        country="UK",
        is_primary=True,
    )
)

address_2 = ORM.insert_address(
    AddressAddDTO(
        user_id=user_1.id,
        street="Main St 12",
        city="New York",
        country="USA",
    )
)

users_with_addresses = ORM.select_users_with_addresses()
users_with_addresses_DTO = [
    UserRelDTO.model_validate(u, from_attributes=True) for u in users_with_addresses
]
print("\n--------------------------")
print(users_with_addresses_DTO)
print("--------------------------\n")


user_2 = ORM.insert_user(
    UserAddDTO(
        username="Alexey",
        email="alexey@example.com",
        description="student",
    )
)

address_3 = ORM.insert_address(
    AddressAddDTO(
        user_id=user_2.id,
        street="Oxford Street",
        city="London",
        country="UK",
    )
)

product_1 = ORM.insert_product(
    ProductAddDTO(
        title="IPhone 17",
        price=170000,
    )
)

product_2 = ORM.insert_product(
    ProductAddDTO(
        title="IPhone 16",
        price=140000,
    )
)

product_3 = ORM.insert_product(
    ProductAddDTO(
        title="IPhone 15 Pro",
        price=150000,
    )
)

product_4 = ORM.insert_product(
    ProductAddDTO(
        title="AirPods Pro 3",
        price=15000,
    )
)

product_5 = ORM.insert_product(
    ProductAddDTO(
        title="Air Pods Pro 2",
        price=10000,
    )
)

cart_1 = ORM.insert_cart(
    CartAddDTO(
        customer_id=user_1.id,
        delivery_address_id=address_1.id,
    )
)

cart_2 = ORM.insert_cart(
    CartAddDTO(
        customer_id=user_1.id,
        delivery_address_id=address_2.id,
    )
)

cart_3 = ORM.insert_cart(
    CartAddDTO(
        customer_id=user_1.id,
        delivery_address_id=address_2.id,
    )
)

cart_4 = ORM.insert_cart(
    CartAddDTO(
        customer_id=user_2.id,
        delivery_address_id=address_3.id,
    )
)

cart_5 = ORM.insert_cart(
    CartAddDTO(
        customer_id=user_2.id,
        delivery_address_id=address_3.id,
    )
)

order_position_1_in_cart_1 = ORM.insert_cart_product(
    CartProductAddDTO(
        cart_id=cart_1.id,
        product_id=product_1.id,
    )
)

order_position_2_in_cart_1 = ORM.insert_cart_product(
    CartProductAddDTO(
        cart_id=cart_1.id,
        product_id=product_2.id,
    )
)

order_position_1_in_cart_2 = ORM.insert_cart_product(
    CartProductAddDTO(
        cart_id=cart_2.id,
        product_id=product_5.id,
        quantity=3,
    )
)

order_position_1_in_cart_3 = ORM.insert_cart_product(
    CartProductAddDTO(
        cart_id=cart_3.id,
        product_id=product_4.id,
        quantity=5,
    )
)

order_position_1_in_cart_4 = ORM.insert_cart_product(
    CartProductAddDTO(
        cart_id=cart_4.id,
        product_id=product_3.id,
    )
)

order_position_1_in_cart_5 = ORM.insert_cart_product(
    CartProductAddDTO(
        cart_id=cart_5.id,
        product_id=product_1.id,
    )
)

carts_with_products = ORM.select_carts_with_products()
carts_with_products_DTO = [
    CartRelDTO.model_validate(c, from_attributes=True) for c in carts_with_products
]
print("\n--------------------------")
print(carts_with_products_DTO)
print("--------------------------\n")
