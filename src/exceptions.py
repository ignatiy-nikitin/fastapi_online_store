from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Server error'

    def __init__(self, status_code=None, detail=None, **kwargs) -> None:
        if status_code is None:
            status_code = self.status_code
        if detail is None:
            detail = self.detail
        super().__init__(status_code=status_code, detail=detail, **kwargs)


class PermissionDeniedException(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'User does not have permissions to create, update, or delete this resource. Permission denied.'
