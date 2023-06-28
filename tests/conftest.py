import os
import pathlib
import shutil

import fakeredis
import pytest
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, drop_database, create_database

from .databases import Session

os.environ['POSTGRES_DB'] = 'fastapi_online_store_test'
os.environ['JWT_SECRET_KEY'] = 'fastapi_online_store_test123'
os.environ['STATIC_FILES_DIR'] = os.path.join(pathlib.Path(__file__).parent, 'static_files_tmp')

from settings import DB_URI

import db as db_database

from . import factories


@pytest.fixture(scope='session')
def testapp():
    from main import app
    yield app


@pytest.fixture(scope='session', autouse=True)
def redis():
    fake_redis = fakeredis.FakeStrictRedis(version=6)
    FastAPICache.init(RedisBackend(fake_redis), prefix='fastapi-cache')
    yield fake_redis


@pytest.fixture(scope='function')
def client(testapp):
    client = TestClient(testapp)
    yield client


@pytest.fixture(scope='session')
def db():
    if database_exists(DB_URI):
        drop_database(DB_URI)
    create_database(DB_URI)
    db_database.create_all_db_tables()
    engine = create_engine(DB_URI)
    Session.configure(bind=engine)
    yield
    drop_database(DB_URI)


@pytest.fixture(scope='session', autouse=True)
def static_files_dir():
    from pathlib import Path
    Path(os.environ['STATIC_FILES_DIR']).mkdir(parents=True, exist_ok=True)
    yield
    shutil.rmtree(os.environ['STATIC_FILES_DIR'])


@pytest.fixture(scope='function', autouse=True)
def db_session(db):
    session = Session()
    session.begin_nested()
    yield session
    session.rollback()


@pytest.fixture
def product(db_session):
    return factories.ProductFactory()


@pytest.fixture
def product_image(db_session, tmp_file):
    path = os.path.split(tmp_file.name)[1]
    return factories.ProductImageFactory(path=path)


@pytest.fixture
def cart(db_session):
    return factories.CartFactory(user=factories.UserClientFactory())


@pytest.fixture
def cart_item(db_session):
    return factories.CartItemFactory(
        cart=factories.CartFactory(
            user=factories.UserClientFactory(),
        ),
        product=factories.ProductFactory(),
    )


@pytest.fixture
def order(db_session, user_client, cart):
    return factories.OrderFactory(
        user=factories.UserClientFactory(),
        cart=factories.CartFactory(
            user=factories.UserClientFactory(),
        ),
    )


@pytest.fixture
def user(db_session):
    return factories.UserFactory()


@pytest.fixture
def user_client(db_session):
    return factories.UserClientFactory()


@pytest.fixture
def user_operator(db_session):
    return factories.UserOperatorFactory()


@pytest.fixture
def user_admin(db_session):
    return factories.UserAdminFactory()


@pytest.fixture
def product_image_file():
    file_path = os.path.join(pathlib.Path(__file__).parent, 'test_static_files', 'logo-teal.png')
    f = open(file_path, 'rb')
    yield f
    f.close()


@pytest.fixture
def tmp_file(product_image_file):
    from settings import STATIC_FILES_DIR
    f = open(os.path.join(STATIC_FILES_DIR, 'logo-teal.png'), 'w+')
    yield f
    f.close()
