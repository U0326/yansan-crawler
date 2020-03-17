import logging

from src.main.video.common.accessor import video_info_accessor
from src.main.video.youtube import accessor as youtube
from src.main.db import video_repository
from src.main.video.youtube.youtube_video_info import YoutubeVideoInfo
from src.main.video.niconico.niconico_video_info import NicoNicoVideoInfo
from src.main.video.common.exception.exceptions import VideoAccessError

logger = logging.getLogger(__name__)


def crawl():
    ids = youtube.take_all_video_ids()
    for _id in ids:
        if video_repository.exists(_id):
            continue
        try:
            youtube_info, niconico_info = video_info_accessor.take_video_info(_id)
        except VideoAccessError:
            logger.error(
                'An error occurred while getting video information. YouTube video_id: %s', _id, exc_info=True)
            continue
        _save_video_info(youtube_info, niconico_info)


def _save_video_info(youtube_info: YoutubeVideoInfo, niconico_info: NicoNicoVideoInfo):
    tags = list(set(youtube_info.tags).union(niconico_info.tags))
    video_repository.save(youtube_info.title, youtube_info.video_id, youtube_info.published_at, tags)


if __name__ == '__main__':
    crawl()
