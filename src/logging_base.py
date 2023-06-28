import logging

from settings import LOG_LEVEL, LOG_FILE

LOG_FORMAT = '%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d'


def configure_logging():
    logging.basicConfig(filename=LOG_FILE, filemode='a', level=LOG_LEVEL, format=LOG_FORMAT)
