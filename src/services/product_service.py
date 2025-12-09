from litestar.exceptions import NotFoundException, HTTPException

from repositories.product_repository import ProductRepository
from schemas import ProductDTO, ProductAddDTO, ProductUpdateDTO


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def get_by_id(self, product_id: int) -> ProductDTO:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundException(detail=f"Product with ID {product_id} not found")
        return ProductDTO.model_validate(product)

    async def create(self, product_data: ProductAddDTO) -> ProductDTO:
        try:
            product = await self.product_repo.create(product_data)
            await self.product_repo.session.commit()
        except:
            await self.product_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"Product create error")
    
        return ProductDTO.model_validate(product)

    async def delete(self, product_id: int) -> None:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundException(detail=f"Product with ID {product_id} not found")

        try:
            await self.product_repo.delete(product)
            await self.product_repo.session.commit()
        except:
            await self.product_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"Product delete error")

    async def update(self, product_id: int, product_data: ProductUpdateDTO) -> ProductDTO:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundException(detail=f"Product with ID {product_id} not found")

        if product_data.title is not None:
            existing_product = await self.product_repo.get_by_title(product_data.title)
            if existing_product and existing_product.id != product.id:
                raise HTTPException(status_code=409, detail=f"Title {product_data.title} is already used by another product")

        try:
            await self.product_repo.update(product, product_data)
            await self.product_repo.session.commit()
        except:
            await self.product_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"Product update error")    

        return ProductDTO.model_validate(product)

    async def get_by_title(self, title: str) -> ProductDTO:
        product = await self.product_repo.get_by_title(title)
        if not product:
            raise NotFoundException(detail=f"Product with title {title} not found")
        return ProductDTO.model_validate(product)
