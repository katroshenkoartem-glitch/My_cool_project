from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from ..repositories.product_repository import ProductRepository
from ..schemas.cart import CartResponse, CartItemCreate, CartItem, CartItemUpdate
from fastapi import HTTPException, status


class CartService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)

    def add_to_cart(
        self, cart_data: Dict[int, int], item: CartItemCreate
    ) -> Dict[int, int]:
        product = self.repository.get_by_id(item.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found",
            )
        if item.product_id in cart_data:
            cart_data[item.product_id] += item.quantity
        else:
            cart_data[item.product_id] = item.quantity
        return cart_data

    def update_cart_item(
        self, cart_data: Dict[int, int], item: CartItemUpdate
    ) -> Dict[int, int]:
        if item.product_id not in cart_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not in cart",
            )
        if item.quantity <= 0:
            del cart_data[item.product_id]
        else:
            cart_data[item.product_id] = item.quantity
        return cart_data

    def remove_from_cart(
        self, cart_data: Dict[int, int], product_id: int
    ) -> Dict[int, int]:
        if product_id not in cart_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not in cart",
            )
        del cart_data[product_id]
        return cart_data

    def get_cart_details(self, cart_data: Dict[int, int]) -> CartResponse:
        # Исправлено: добавлены все три обязательных поля для пустой корзины
        if not cart_data:
            return CartResponse(items=[], total_quantity=0, total_price=0.0)

        product_ids = list(cart_data.keys())
        # Исправлено: используем self.repository вместо self.product_repository
        products = self.repository.get_multiple_by_ids(product_ids)
        products_dict = {product.id: product for product in products}

        cart_items = []
        total_price = 0.0
        total_items = 0

        for product_id, quantity in cart_data.items():
            if product_id in products_dict:
                product = products_dict[product_id]
                subtotal = product.price * quantity

                cart_item = CartItem(
                    product_id=product.id,
                    name=product.name,
                    price=product.price,
                    quantity=quantity,
                    subtotal=subtotal,
                    image_url=product.image_url,
                )
                cart_items.append(cart_item)
                total_price += subtotal
                total_items += quantity

        # Исправлено: передаем имена полей в строгом соответствии со схемой CartResponse
        return CartResponse(
            items=cart_items,
            total_price=round(total_price, 2),
            total_quantity=total_items,
        )
