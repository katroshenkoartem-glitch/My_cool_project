from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .category import CategoryResponse


class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=200,)

    description: Optional[str] = Field(None, description='Product description')
    price: float = Field(..., gt=0,
                         description='Product price(must be positive)')

    category_id: int = Field(..., description='ID of the product category')
    image_url: Optional[str] = Field(
        None, description='URL of the product image')


class ProductCreate(ProductBase):
    pass


class ProductResponse(BaseModel):
    id: int = Field(..., description='Unique Product ID')
    name: str
    description: Optional[str]
    price: float
    category_id: int
    image_url: Optional[str]
    created_at: datetime
    category: CategoryResponse = Field(...,
                                       description='Category of the product')

    class Config:
        form_attributes = True


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int = Field(..., description='Total number of products')
