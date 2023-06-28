import datetime
from decimal import Decimal

from pydantic import PositiveInt

from orders import models
from pydantic_base import BasePDModel


class OrderRead(BasePDModel):
    id: PositiveInt
    created_dt: datetime.datetime
    delivery_dt: datetime.datetime
    address: str
    status: models.OrderStatus
    total_cost: Decimal
