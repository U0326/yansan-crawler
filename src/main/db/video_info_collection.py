from src.main.db import _db
_video_info_collection = _db.video_info


def exists(video_id):
    return _video_info_collection.count_documents({'id': video_id}) > 0


def _save_video_info(video_info):
    _video_info_collection.insert_one(video_info)
