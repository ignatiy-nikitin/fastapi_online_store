import logging

from fastapi import status
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from settings import DEBUG

logger = logging.getLogger(__name__)


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> JSONResponse:
        try:
            response = await call_next(request)
        except ValidationError as e:
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={'detail': e.errors()},
            )
        except ValueError as e:
            if DEBUG:
                raise e
            logger.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={'detail': [{'msg': 'Unknown', 'loc': ['Unknown'], 'type': 'Unknown'}]},
            )
        except Exception as e:
            if DEBUG:
                raise e
            logger.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={'detail': [{'msg': 'Unknown', 'loc': ['Unknown'], 'type': 'Unknown'}]},
            )

        return response
