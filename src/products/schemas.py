from decimal import Decimal

from pydantic_base import BasePDModel


class ProductCreateUpdate(BasePDModel):
    title: str
    description: str
    price: Decimal
