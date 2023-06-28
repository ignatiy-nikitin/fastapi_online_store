from sqlalchemy import Integer, ForeignKey, Column, Numeric
from sqlalchemy.orm import relationship

from db import BaseDBModel


class Cart(BaseDBModel):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    # relationships
    user = relationship('User', back_populates='cart')
    cart_items = relationship('CartItem', back_populates='cart')
    order = relationship('Order', back_populates='cart')

    @property
    def total_cost(self):
        return sum(cart_item.quantity * cart_item.price for cart_item in self.cart_items)


class CartItem(BaseDBModel):
    __tablename__ = 'cart_item'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    product_id = Column(ForeignKey('product.id'))
    cart_id = Column(ForeignKey('cart.id'))
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)

    # relationships
    product = relationship('Product', back_populates='cart_items')
    cart = relationship('Cart', back_populates='cart_items')
