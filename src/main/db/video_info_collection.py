from typing import List

from src.main.db import _db
_video_info_collection = _db.video_info


def exists(video_id):
    return _video_info_collection.count_documents({'id': video_id}) > 0


def take_all_video_ids() -> List[str]:
    documents = _video_info_collection.find({}, {'_id': 0, 'id': 1})
    return [document['id'] for document in documents]


def _save_video_info(video_info):
    _video_info_collection.insert_one(video_info)


def _delete_video_info(video_ids: list):
    _video_info_collection.delete_many({'id': {'$in': video_ids}})
