import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_pagination import add_pagination
from redis import asyncio as aioredis

import db
from api import api_router
from logging_base import configure_logging
from middlewares import ExceptionMiddleware
from settings import PORT, FASTAPI_LOGGING_LEVEL, DEBUG, REDIS_HOST

configure_logging()

app = FastAPI(
    title='OnlineStoreAPI',
    description='Online store API, FastAPI based',
    version='1.0',
    root_path='/api/v1',
    openapi_url='/docs/openapi.json',
    # docs_url='/docs',
    # redoc_url='/redoc',
)
app.include_router(api_router)
app.add_middleware(ExceptionMiddleware)

app.mount('/api/v1', app=app)

add_pagination(app)


def before_startup_server():
    if DEBUG:
        db.create_all_db_tables()
    redis = aioredis.from_url(REDIS_HOST, encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


@app.on_event('startup')
def startup_event():
    before_startup_server()


if __name__ == '__main__':
    before_startup_server()
    uvicorn.run(app, host='0.0.0.0', port=PORT, log_level=FASTAPI_LOGGING_LEVEL)
