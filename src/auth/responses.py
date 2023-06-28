from pydantic import EmailStr, PositiveInt

from auth import models
from pydantic_base import BasePDModel


class UserRead(BasePDModel):
    email: EmailStr
    name: str
    age: PositiveInt
    role: models.UserRoles


class Token(BasePDModel):
    access_token: str
    token_type: str = 'bearer'
