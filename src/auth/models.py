import enum

from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import relationship

from auth import utils
from db import BaseDBModel


class UserRoles(enum.Enum):
    client = 'client'
    operator = 'operator'
    admin = 'admin'


class User(BaseDBModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    role = Column(Enum(UserRoles), nullable=False)

    # relationships
    cart = relationship('Cart', uselist=False, back_populates='user')
    orders = relationship('Order', back_populates='user')

    def check_password(self, password: str):
        return utils.verify_password(password, self.password)

    @property
    def jwt_token(self):
        toke_payload_data = {
            'email': self.email,
            'name': self.name,
            'age': self.age,
            'role': self.role.value,
            'username': self.username,
        }
        return utils.gen_jwt_token(toke_payload_data)
