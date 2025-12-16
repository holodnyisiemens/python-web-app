# from sqlalchemy import select
# from sqlalchemy.orm import selectinload

# from database import session_factory
# from models import Address, Cart, CartProduct, Product, User
# from schemas import (
#     AddressAddDTO,
#     CartAddDTO,
#     CartProductAddDTO,
#     ProductAddDTO,
#     UserAddDTO,
# )


# class ORM:
#     @staticmethod
#     def insert_user(data: UserAddDTO):
#         with session_factory() as session:
#             user = User(**data.model_dump())
#             session.add(user)
#             session.commit()
#             session.refresh(user)
#             return user

#     @staticmethod
#     def insert_address(data: AddressAddDTO):
#         with session_factory() as session:
#             address = Address(**data.model_dump())
#             session.add(address)
#             session.commit()
#             session.refresh(address)
#             return address

#     @staticmethod
#     def select_users_with_addresses():
#         with session_factory() as session:
#             query = select(User).options(selectinload(User.addresses))
#             res = session.execute(query)
#             result = res.unique().scalars().all()
#             return result

#     @staticmethod
#     def insert_product(data: ProductAddDTO):
#         with session_factory() as session:
#             product = Product(**data.model_dump())
#             session.add(product)
#             session.commit()
#             session.refresh(product)
#             return product

#     @staticmethod
#     def insert_cart(data: CartAddDTO):
#         with session_factory() as session:
#             cart = Cart(**data.model_dump())
#             session.add(cart)
#             session.commit()
#             session.refresh(cart)
#             return cart

#     @staticmethod
#     def insert_cart_product(data: CartProductAddDTO):
#         with session_factory() as session:
#             order_position = CartProduct(**data.model_dump())
#             session.add(order_position)
#             session.commit()
#             session.refresh(order_position)
#             return order_position

#     @staticmethod
#     def select_carts_with_products():
#         with session_factory() as session:
#             query = select(Cart).options(selectinload(Cart.products))
#             res = session.execute(query)
#             result = res.unique().scalars().all()
#             return result
