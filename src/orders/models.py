import datetime
import enum

from sqlalchemy import Integer, ForeignKey, Column, Numeric, DateTime, String, Enum
from sqlalchemy.orm import relationship

from db import BaseDBModel


class OrderStatus(enum.Enum):
    created = 'created'
    delivered = 'delivered'
    processed = 'processed'
    cancelled = 'cancelled'


class Order(BaseDBModel):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    created_dt = Column(DateTime, default=datetime.datetime.now())
    delivery_dt = Column(DateTime, default=datetime.datetime.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    address = Column(String, nullable=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    status = Column(Enum(OrderStatus), nullable=False)
    total_cost = Column(Numeric, default=0)

    # relationships
    user = relationship('User', back_populates='orders')
    cart = relationship('Cart', uselist=False, back_populates='order')
