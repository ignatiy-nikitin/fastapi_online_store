from sqlalchemy import Column, String, Text, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from db import BaseDBModel


class Product(BaseDBModel):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, default='')
    price = Column(Numeric, nullable=False)

    # relationships
    images = relationship('ProductImage', back_populates='product')
    cart_items = relationship('CartItem', back_populates='product')


class ProductImage(BaseDBModel):
    __tablename__ = 'product_image'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    product_id = Column(ForeignKey('product.id'))
    path = Column(String, nullable=False)

    # relationships
    product = relationship('Product', back_populates='images')
