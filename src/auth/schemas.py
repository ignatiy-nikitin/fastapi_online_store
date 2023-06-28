from pydantic import EmailStr, PositiveInt, validator, Field

from auth import utils, models
from pydantic_base import BasePDModel


class UserRegister(BasePDModel):
    email: EmailStr
    username: str
    password: str
    name: str
    age: PositiveInt
    role: models.UserRoles = Field(models.UserRoles.client, const=True)

    @validator('password', pre=True, always=True)
    def password_required(cls, v):
        return utils.get_password_hash(v)


class UserUpdateBase(BasePDModel):
    password: str
    name: str
    age: PositiveInt

    @validator('password', pre=True, always=True)
    def password_required(cls, v):
        return utils.get_password_hash(v)


class UserUpdate(UserUpdateBase):
    role: models.UserRoles
