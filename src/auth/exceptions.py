from fastapi import status

from exceptions import BaseHTTPException


class UserWithThisUsernameAlreadyExistsException(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'User with username already exists.'


class InvalidLoginDataException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid login data.'


class CredentialsException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Could not validate credentials.'
