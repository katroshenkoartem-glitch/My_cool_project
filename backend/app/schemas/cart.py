from pydantic import BaseModel, Field
from typing import Optional


class CartItemBase(BaseModel):
    product_id: int = Field(..., description='ID of the product')
    quantity: int = Field(..., gt=0,
                          description='Quantity of the product in cart')


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    product_id: int = Field(..., description='ID of the product')
    quantity: Optional[int] = Field(
        ..., gt=0, description='Updated quantity of the product in cart')


class CartItem(BaseModel):
    product_id: int
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")
    quantity: int = Field(..., description="Quantity in cart")
    subtotal: float = Field(...,
                            description="Total price for this item (price * quantity)")
    image_url: Optional[str] = Field(None, description="Product image URL")


class CartResponse(BaseModel):
    items: list[CartItem] = Field(..., description="List of items in the cart")
    total_quantity: int = Field(...,
                                description="Total quantity of items in the cart")
    total_price: float = Field(...,
                               description="Total price of all items in the cart")
