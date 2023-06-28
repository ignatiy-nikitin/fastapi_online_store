import os
import pathlib
from pathlib import Path

from dotenv import load_dotenv

env_file = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_file)

DEBUG = os.environ.get('DEBUG') == 'True'

ROOT_DIR = pathlib.Path(__file__).parent.resolve().parents[0]

STATIC_FILES_DIR = os.environ.get('STATIC_FILES_DIR', os.path.join(ROOT_DIR, 'static_files'))
Path(STATIC_FILES_DIR).mkdir(parents=True, exist_ok=True)

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FILE = os.environ.get('LOG_FILE', os.path.join(ROOT_DIR, 'logs', 'logs.log'))
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

try:
    PORT = int(os.environ.get('PORT', 8000))
    FASTAPI_LOGGING_LEVEL = os.environ.get('FASTAPI_LOGGING_LEVEL', 'info')

    POSTGRES_DB = os.environ['POSTGRES_DB']
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
    DB_HOST = os.environ.get('DB_HOST', 'localhost')

    DB_URI = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}/{POSTGRES_DB}'

    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS512')
    JWT_ACCESS_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 240))

    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_FROM = os.environ['MAIL_FROM']
    MAIL_PORT = int(os.environ['MAIL_PORT'])
    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_FROM_NAME = os.environ.get('MAIL_FROM_NAME', 'Fast Api Online Store')

    REDIS_HOST = os.environ.get('REDIS_HOST', 'redis://localhost')

except KeyError as e:
    raise AttributeError(f'Set all variables in .env file. Variable required: {e}')
