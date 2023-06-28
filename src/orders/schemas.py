import datetime

from pydantic_base import BasePDModel


class OrderCreate(BasePDModel):
    delivery_dt: datetime.datetime
    address: str
