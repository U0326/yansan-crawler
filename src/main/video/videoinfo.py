import os
import logging
import re
from typing import Tuple

from src.main.video.niconico import const as niconico_const
from src.main.video.youtube.youtube_video_info import YoutubeVideoInfo
from src.main.video.niconico.niconico_video_info import NicoNicoVideoInfo

logger = logging.getLogger(__name__)


def take_video_info(youtube_id) -> Tuple[YoutubeVideoInfo, NicoNicoVideoInfo]:
    youtube_info = YoutubeVideoInfo(youtube_id)
    if not youtube_info:
        return
    niconico_id = _take_niconico_video_id(youtube_info)
    if not niconico_id:
        return
    niconico_info = NicoNicoVideoInfo(niconico_id)
    return youtube_info, niconico_info


def _take_niconico_video_id(info):
    for text in [info.description, info.comment_of_poster]:
        matched = re.match(
            '.*' + re.escape(niconico_const.VIDEO_RESOURCE_PREFIX) + '([a-z0-9]+).*',
            text.replace(os.linesep, ' '))
        if matched:
            niconico_id = matched.group(1)
            logger.debug('niconico id: ' + niconico_id)
            return niconico_id
    logger.warning('Niconico video ID not exists. title: ' + info.title)
