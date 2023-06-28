import functools

from exceptions import PermissionDeniedException


def permission_handler(status_code=None, detail=None):
    def _permission_handler(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            permission_check_result = func(*args, **kwargs)
            if not permission_check_result:
                raise PermissionDeniedException(status_code, detail)
            return permission_check_result

        return inner

    return _permission_handler
