from pymongo import MongoClient
from src.main import config

_client = MongoClient(config.DB_HOST, config.MONGO_PORT)
_db = _client.yansan_db
_video_info_collection = _db.video_info
_tags_collection = _db.tags
_processing_collection = _db.processing


def exists_video_id(video_id):
    return _video_info_collection.find({'id': video_id}).count() > 0


def save_video_info(video_info):
    _video_info_collection.insert_one(video_info)


def save_tag_and_video_id(tag, video_id):
    _tags_collection.update({'tag': tag}, {'$push': {'video_id': video_id}}, True)


def save_next_page_token(next_page_token):
    _processing_collection.update({}, {'next_page_token': next_page_token}, True)


def take_next_page_token():
    result = _processing_collection.find_one()
    if result:
        return result.get('next_page_token')
    else:
        return
