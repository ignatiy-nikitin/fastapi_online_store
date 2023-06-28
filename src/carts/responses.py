from decimal import Decimal

from pydantic_base import BasePDModel


class CartRead(BasePDModel):
    id: int
    user_id: int


class CartItemRead(BasePDModel):
    id: int
    product_id: int
    cart_id: int
    quantity: int
    price: Decimal
