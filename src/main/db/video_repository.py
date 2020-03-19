from typing import List

from src.main.db.video_info_collection import *
from src.main.db.video_info_collection import _save_video_info
from src.main.db.video_info_collection import _delete_video_info
from src.main.db.tags_collection import *
from src.main.db.tags_collection import _save_tag_and_video_id
from src.main.db.tags_collection import _delete_video_ids
from src.main.db.tags_collection import _delete_tag_if_no_video_id


def save(title: str, video_id: str, published_at: str, tags: List[str]):
    _save_video_info(
        {
            'title': title,
            'id': video_id,
            'published_at': published_at,
            'tags': tags
        }
    )
    for tag in tags:
        _save_tag_and_video_id(tag, video_id)


def delete(video_ids: List[str]):
    _delete_video_info(video_ids)
    _delete_video_ids(video_ids)
    _delete_tag_if_no_video_id()
