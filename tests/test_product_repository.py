import pytest

from models import Product
from schemas import ProductAddDTO, ProductUpdateDTO, ProductDTO
from repositories.product_repository import ProductRepository


product_data_1 = ProductAddDTO(
    title="IPhone 17",
    description="newest IPhone",
    price=150000,
    stock_qty=10,
)

product_data_2 = ProductAddDTO(
    title="IPhone 16",
    description="previous IPhone",
    price=100000,
    stock_qty=10,
)


class TestProductRepository:
    async def _create_test_product(self, product_repository: ProductRepository, product_data: ProductAddDTO) -> Product:
        product = await product_repository.create(product_data)
        return product

    @pytest.mark.asyncio
    async def test_create_product(self, product_repository: ProductRepository):
        product = await self._create_test_product(product_repository, product_data_1)

        assert product.id is not None
        assert product.title == product_data_1.title
        assert product.description == product_data_1.description
        assert product.price == product_data_1.price
        assert product.stock_qty == product_data_1.stock_qty

    @pytest.mark.asyncio
    async def test_update_product(self, product_repository: ProductRepository):
        product = await self._create_test_product(product_repository, product_data_1)

        new_product_data = ProductUpdateDTO(title="Updated")

        await product_repository.update(product, new_product_data)

        updated_product = await product_repository.get_by_id(product.id)
        
        assert updated_product.title == new_product_data.title

        assert updated_product.id == product.id
        assert updated_product.description == product.description
        assert updated_product.price == product.price
        assert updated_product.stock_qty == product.stock_qty

    @pytest.mark.asyncio
    async def test_delete_product(self, product_repository: ProductRepository):
        product = await self._create_test_product(product_repository, product_data_1)
        await product_repository.delete(product)

        found_product = await product_repository.get_by_id(product.id)
        assert found_product is None

    @pytest.mark.asyncio
    async def test_get_all_products(self, product_repository: ProductRepository):
        await self._create_test_product(product_repository, product_data_1)
        await self._create_test_product(product_repository, product_data_2)

        products_list = await product_repository.get_all()

        product_titles = [product.title for product in products_list]

        assert len(products_list) == 2
        assert product_titles[0] == product_data_1.title
        assert product_titles[1] == product_data_2.title
