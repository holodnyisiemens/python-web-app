import pytest

from schemas import ProductAddDTO, ProductUpdateDTO, ProductDTO
from repositories.product_repository import ProductRepository


class TestProductRepository:
    @pytest.mark.asyncio
    async def test_create_product(self, product_repository: ProductRepository, product_data_1: ProductAddDTO):
        product = await product_repository.create(product_data_1)

        assert product.id is not None
        assert product.title == product_data_1.title
        assert product.description == product_data_1.description
        assert product.price == product_data_1.price
        assert product.stock_qty == product_data_1.stock_qty

    @pytest.mark.asyncio
    async def test_update_product(self, product_repository: ProductRepository, product_1: ProductDTO):
        new_product_data = ProductUpdateDTO(title="Updated")

        await product_repository.update(product_1, new_product_data)

        updated_product = await product_repository.get_by_id(product_1.id)
        
        assert updated_product.title == new_product_data.title

        assert updated_product.id == product_1.id
        assert updated_product.description == product_1.description
        assert updated_product.price == product_1.price
        assert updated_product.stock_qty == product_1.stock_qty

    @pytest.mark.asyncio
    async def test_delete_product(self, product_repository: ProductRepository, product_1: ProductDTO):
        await product_repository.delete(product_1)

        found_product = await product_repository.get_by_id(product_1.id)
        assert found_product is None

    @pytest.mark.asyncio
    async def test_get_all_products(self, product_repository: ProductRepository, product_1: ProductDTO, product_2: ProductDTO):
        products_list = await product_repository.get_all()

        product_titles = [product.title for product in products_list]

        assert len(products_list) == 2
        assert product_titles[0] == product_1.title
        assert product_titles[1] == product_2.title
