from pymongo import MongoClient
from src.main import config

client = MongoClient(config.DB_HOST, config.MONGO_PORT)
db = client.yansan_db
video_info_collection = db.video_info
tags_collection = db.tags
processing_collection = db.processing


def exists_video_id(video_id):
    return video_info_collection.find({'id': video_id}).count() > 0


def save_video_info(video_info):
    video_info_collection.insert_one(video_info)


def push_id_per_tag(tag, video_id):
    tags_collection.update({'tag': tag}, {'$push': {'video_id': video_id}}, True)


def save_next_page_token(next_page_token):
    processing_collection.update({}, {'next_page_token': next_page_token}, True)


def get_next_page_token():
    result = processing_collection.find_one()
    if result:
        return result.get('next_page_token')
    else:
        return
