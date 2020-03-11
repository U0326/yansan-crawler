from collections import namedtuple
import os
import logging
import re
from src.main.video.youtube.youtube_video_info import YoutubeVideoInfo
from src.main.video.niconico import accessor as niconico
from src.main.video.niconico import const as niconico_const

NiconicoVideoInfo = namedtuple('NiconicoVideoInfo', ('description', 'tags'))
VideoInfo = namedtuple('VideoInfo', ('title', 'youtube_description', 'youtube_tags',
                                     'niconico_description', 'niconico_tags', 'published_at'))
logger = logging.getLogger(__name__)


def take_video_info(youtube_id):
    youtube_info = YoutubeVideoInfo(youtube_id)
    if not youtube_info:
        return
    niconico_id = take_niconico_video_id(youtube_info)
    if not niconico_id:
        return
    niconico_info = niconico.take_video_info(niconico_id)
    niconico_info = filter_niconico_info(niconico_info)
    return VideoInfo(youtube_info.title, youtube_info.description, youtube_info.tags,
                     niconico_info.description, niconico_info.tags, youtube_info.published_at)


def take_niconico_video_id(info):
    for text in [info.description, info.comment_of_poster]:
        matched = re.match(
            '.*' + re.escape(niconico_const.VIDEO_RESOURCE_PREFIX) + '([a-z0-9]+).*',
            text.replace(os.linesep, ' '))
        if matched:
            niconico_id = matched.group(1)
            logger.debug('niconico id: ' + niconico_id)
            return niconico_id
    logger.warning('Niconico video ID not exists. title: ' + info.title)


def filter_niconico_info(video_info):
    description = niconico.take_description(video_info)
    tags = niconico.take_tags_exclude_category(video_info)
    logger.debug('niconico description: ' + description.replace(os.linesep, ' '))
    logger.debug('niconico tags: ' + str(tags))
    return NiconicoVideoInfo(description, tags)
