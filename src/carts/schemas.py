from pydantic import PositiveInt

from pydantic_base import BasePDModel


class CartItemCreate(BasePDModel):
    product_id: int
    quantity: PositiveInt


class CartItemUpdate(BasePDModel):
    quantity: PositiveInt
