from sqlalchemy.orm import Session
from typing import List, Optional
from ..repositories.product_repository import ProductRepository
from ..repositories.category_repository import CategoryRepository
from ..schemas.product import ProductResponse, ProductCreate, ProductListResponse
from fastapi import HTTPException, status


class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    def get_all_products(self) -> ProductListResponse:
        products = self.repository.get_all()
        products_response = ProductListResponse(
            [ProductResponse.model_validate(prod) for prod in products])
        return ProductListResponse(products=products_response, total=len(products_response.products))

    def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found",
            )
        return ProductResponse.model_validate(product)

    def get_products_by_category(self, category_id: int) -> ProductListResponse:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )
        products = self.repository.get_by_category(category_id)
        products_response = ProductListResponse(
            [ProductResponse.model_validate(prod) for prod in products])
        return ProductListResponse(products=products_response, total=len(products_response.products))

    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        category = self.category_repository.get_by_id(product_data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {product_data.category_id} not found",
            )
        product = self.repository.create(product_data)
        return ProductResponse.model_validate(product)
