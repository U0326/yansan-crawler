import logging

from src.main.video.common.accessor import video_info_accessor
from src.main.video.youtube import accessor as youtube
from src.main.db import video_repository
from src.main.video.youtube.youtube_video_info import YoutubeVideoInfo
from src.main.video.niconico.niconico_video_info import NicoNicoVideoInfo
from src.main.video.common.exception.exceptions import VideoAccessError

logger = logging.getLogger(__name__)


def crawl():
    while True:
        next_page_token = video_repository.get_next_page_token()
        next_page_token, ids = youtube.take_video_ids(next_page_token)
        for _id in ids:
            if video_repository.exists_video_id(_id):
                continue
            try:
                youtube_info, niconico_info = video_info_accessor.take_video_info(_id)
            except VideoAccessError:
                logger.error(
                    'An error occurred while getting video information. YouTube video_id: %s', _id, exc_info=True)
                continue
            _save_video_info(youtube_info, niconico_info)
        video_repository.save_next_page_token(next_page_token)
        if not next_page_token:
            break


def _save_video_info(youtube_info: YoutubeVideoInfo, niconico_info: NicoNicoVideoInfo):
    tags = list(set(youtube_info.tags).union(niconico_info.tags))
    video_repository.save_video_info(
        {
            'title': youtube_info.title,
            'id': youtube_info.video_id,
            'published_at': youtube_info.published_at,
            'tags': tags
        }
    )
    for tag in tags:
        video_repository.push_id_per_tag(tag, youtube_info.video_id)


if __name__ == '__main__':
    crawl()
