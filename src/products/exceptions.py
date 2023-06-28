from fastapi import status

from exceptions import BaseHTTPException


class ProductNotFoundByIdException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Product not found by id.'


class ProductImageNotFoundByIdException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Product image not found by id.'
