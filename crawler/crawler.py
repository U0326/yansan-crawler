import logging

from video import videoinfo
from video.youtube import accessor as youtube
from tag import tag
from video.db import video_repository

logger = logging.getLogger(__name__)


def crawl():
    while True:
        next_page_token = video_repository.get_next_page_token()
        next_page_token, ids = youtube.take_video_ids(next_page_token)
        save_video_info(ids)
        video_repository.save_next_page_token(next_page_token)
        if not next_page_token:
            break


def save_video_info(ids):
    for video_id in ids:
        if video_repository.exists_video_id(video_id):
            continue
        video_info = videoinfo.take_video_info(video_id)
        if not video_info:
            continue
        tag_frequency = tag.count_tag_appearance(video_info)
        record = {'title': video_info.title, 'id': video_id,
                  'published_at': video_info.published_at, 'tags': tag_frequency}
        video_repository.insert_video_info(record)
        for tag_value in tag_frequency.keys():
            video_repository.push_id_per_tag(tag_value, video_id)


if __name__ == '__main__':
    log_format = '%(asctime)s %(levelname)s %(name)s :%(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)
    crawl()
