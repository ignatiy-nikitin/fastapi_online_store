import datetime

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def gen_jwt_token(toke_payload_data):
    now = datetime.datetime.utcnow()
    exp = (now + datetime.timedelta(seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60)).timestamp()
    toke_payload_data['exp'] = exp
    return jwt.encode(toke_payload_data, settings.JWT_ACCESS_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_jwt_token(token: str):
    return jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
