import logging
import json
import requests
from src.main.video.youtube import const

SEARCH_PATH = '/search'
VIDEOS_PATH = '/videos'
COMMENT_PATH = '/commentThreads'
MAX_RESULTS = 50
logger = logging.getLogger(__name__)


def take_video_ids(next_page_token=None):
    query = {
        'part': 'id',
        'type': 'video',
        'pageToken': next_page_token,
        'maxResults': MAX_RESULTS,
        'channelId': const.YANSAN_CHANNEL_ID,
        'videoDuration': 'long',
        'order': 'date',
        'key': const.API_KEY
    }
    response = requests.get(const.END_POINT + SEARCH_PATH, query)
    response_dict = json.loads(response.content)
    logger.debug(json.dumps(response_dict, indent=4, ensure_ascii=False))

    next_page_token = response_dict['nextPageToken'] if 'nextPageToken' in response_dict else None
    ids = [element['id']['videoId'] for element in response_dict['items']]
    logger.info('search result nextPageToken: ' + str(next_page_token) + ', ' + 'youtube ids: ' + str(ids))
    return next_page_token, ids


def take_video_info(video_id):
    query = {
        'part': 'snippet',
        'id': video_id,
        'key': const.API_KEY
    }
    response = requests.get(const.END_POINT + VIDEOS_PATH, query)
    response_dict = json.loads(response.content)
    logger.debug(json.dumps(response_dict, indent=4, ensure_ascii=False))

    return response_dict['items'][0]['snippet']


def take_comment_of_poster(video_id):
    query = {
        'part': 'snippet',
        'videoId': video_id,
        'textFormat': 'plainText',
        # 投稿者による固定されたコメントは先頭になる。
        'maxResults': 1,
        'key': const.API_KEY
    }
    response = requests.get(const.END_POINT + COMMENT_PATH, query)
    response_dict = json.loads(response.content)
    logger.debug(json.dumps(response_dict, indent=4, ensure_ascii=False))
    if 'items' not in response_dict or len(response_dict['items']) is 0:
        return None

    first_comment = response_dict['items'][0]['snippet']['topLevelComment']['snippet']
    # 投稿者による固定されたコメントが存在する場合、それを返却する。
    return first_comment['textDisplay'] \
        if first_comment['authorChannelId']['value'] == const.YANSAN_CHANNEL_ID \
        else None
