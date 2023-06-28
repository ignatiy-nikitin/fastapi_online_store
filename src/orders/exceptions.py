from fastapi import status

from exceptions import BaseHTTPException


class OrderNotFoundByIdException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Order not found by id.'
