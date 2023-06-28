from fastapi import status

from exceptions import BaseHTTPException


class CartNotFoundByIdException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Cart not found by id.'


class CartItemNotFoundByIdException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Cart item not found by id.'
