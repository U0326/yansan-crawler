from pymongo import MongoClient
from src.main import config

_client = MongoClient(config.DB_HOST, config.MONGO_PORT)
_db = _client.yansan_db
