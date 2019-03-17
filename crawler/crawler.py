import logging

from video import videoinfo
from video.youtube import accessor as youtube
from tag import tag

logger = logging.getLogger(__name__)


def crawl():
    # TODO ページングに対応する必要がある。
    next_page_token, ids = youtube.take_video_ids()
    for youtube_id in ids:
        video_info = videoinfo.take_video_info(youtube_id)
        if not video_info:
            continue
        tag.count_tag_appearance(video_info)


if __name__ == '__main__':
    log_format = '%(asctime)s %(levelname)s %(name)s :%(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)
    crawl()
