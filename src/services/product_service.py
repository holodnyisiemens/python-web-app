from litestar.exceptions import HTTPException
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from src.repositories.product_repository import ProductRepository
from src.schemas import ProductAddDTO, ProductDTO, ProductUpdateDTO


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def get_by_id(self, product_id: int) -> ProductDTO:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found",
            )
        return ProductDTO.model_validate(product)

    async def create(self, product_data: ProductAddDTO) -> ProductDTO:
        try:
            product = await self.product_repo.create(product_data)
            await self.product_repo.session.commit()
        except Exception as exc:
            await self.product_repo.session.rollback()
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Product create error"
            ) from exc

        return ProductDTO.model_validate(product)

    async def delete(self, product_id: int) -> None:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found",
            )

        try:
            await self.product_repo.delete(product)
            await self.product_repo.session.commit()
        except Exception as exc:
            await self.product_repo.session.rollback()
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f"Product with ID {product_id} delete error",
            ) from exc

    async def update(
        self, product_id: int, product_data: ProductUpdateDTO
    ) -> ProductDTO:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found",
            )

        if product_data.title is not None:
            existing_product = await self.product_repo.get_by_title(product_data.title)
            if existing_product and existing_product.id != product.id:
                raise HTTPException(
                    status_code=HTTP_409_CONFLICT,
                    detail=f"Title {product_data.title} is already used by another product",
                )

        try:
            await self.product_repo.update(product, product_data)
            await self.product_repo.session.commit()
        except Exception as exc:
            await self.product_repo.session.rollback()
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f"Product with ID {product_id} update error",
            ) from exc

        return ProductDTO.model_validate(product)

    async def get_by_title(self, title: str) -> ProductDTO:
        product = await self.product_repo.get_by_title(title)
        if not product:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Product with title {title} not found",
            )
        return ProductDTO.model_validate(product)
