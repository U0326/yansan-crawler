from src.main.db import _db
_tags_collection = _db.tags


def _save_tag_and_video_id(tag, video_id):
    _tags_collection.update({'tag': tag}, {'$push': {'video_id': video_id}}, True)
