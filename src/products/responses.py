from decimal import Decimal

from pydantic import PositiveInt

from pydantic_base import BasePDModel


class ProductImageRead(BasePDModel):
    id: PositiveInt
    path: str


class ProductRead(BasePDModel):
    id: int
    title: str
    description: str
    price: Decimal
    images: list[ProductImageRead]


class ProductPagination(BasePDModel):
    total: int
    products: list[ProductRead] = []
