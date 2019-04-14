from collections import namedtuple
import os
import logging
import re
from video.youtube import accessor as youtube
from video.niconico import accessor as niconico
from video.niconico import const as niconico_const

YouTubeVideoInfo = namedtuple('YouTubeVideoInfo', ('title', 'description', 'tags', 'comment_of_poster', 'published_at'))
NiconicoVideoInfo = namedtuple('NiconicoVideoInfo', ('description', 'tags'))
VideoInfo = namedtuple('VideoInfo', ('title', 'youtube_description', 'youtube_tags',
                                     'niconico_description', 'niconico_tags', 'published_at'))
logger = logging.getLogger(__name__)


def take_video_info(youtube_id):
    youtube_info = youtube.take_video_info(youtube_id)
    youtube_info = filter_youtube_info(youtube_id, youtube_info)
    if not youtube_info:
        return
    niconico_id = take_niconico_video_id(youtube_info)
    if not niconico_id:
        return
    niconico_info = niconico.take_vide_info(niconico_id)
    niconico_info = filter_niconico_info(niconico_info)
    return VideoInfo(youtube_info.title, youtube_info.description, youtube_info.tags,
                     niconico_info.description, niconico_info.tags, youtube_info.published_at)


def filter_youtube_info(video_id, video_info):
    title = video_info['title']
    description = video_info['description']
    tags = video_info['tags']
    published_at = video_info['publishedAt']
    comment_of_poster = youtube.take_comment_of_poster(video_id)
    logger.debug('title: ' + title)
    logger.debug('youtube description: ' + description.replace(os.linesep, ' '))
    logger.debug('youtube tags: ' + str(tags))
    logger.debug('publishedAt: ' + published_at)
    logger.debug('comment_of_poster: ' + str(comment_of_poster).replace(os.linesep, ' '))
    return YouTubeVideoInfo(title, description, tags, comment_of_poster, published_at)


def take_niconico_video_id(info):
    for text in info:
        if not hasattr(text, 'replace'):
            continue
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
