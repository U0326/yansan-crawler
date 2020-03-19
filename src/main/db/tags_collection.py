from src.main.db import _db
_tags_collection = _db.tags


def _save_tag_and_video_id(tag, video_id):
    _tags_collection.update({'tag': tag}, {'$push': {'video_id': video_id}}, True)


def _delete_video_ids(video_ids):
    _tags_collection.update_many({}, {'$pullAll': {'video_id': video_ids}})


def _delete_tag_if_no_video_id():
    _tags_collection.delete_many({'video_id': {'$size': 0}})
