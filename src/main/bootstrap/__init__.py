import logging

from src.main import config

log_format = '%(asctime)s %(levelname)s %(name)s :%(message)s'
logging.basicConfig(level=config.LOG_LEVEL, format=log_format)
