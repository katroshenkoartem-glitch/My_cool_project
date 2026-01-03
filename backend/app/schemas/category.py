from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100,
                      description='Category name')
    slug: str = Field(..., min_length=3, max_length=100,
                      description='URL Category name')


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int = Field(..., description='Unique Category ID')

    class Config:
        form_attributes = True
