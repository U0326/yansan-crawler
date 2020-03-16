from pymongo import MongoClient
from src.main import config

_client = MongoClient(config.DB_HOST, config.MONGO_PORT)
_db = _client.yansan_db
_video_info_collection = _db.video_info
_tags_collection = _db.tags


def exists_video_id(video_id):
    return _video_info_collection.count_documents({'id': video_id}) > 0


def save_video_info(video_info):
    _video_info_collection.insert_one(video_info)


def save_tag_and_video_id(tag, video_id):
    _tags_collection.update({'tag': tag}, {'$push': {'video_id': video_id}}, True)
