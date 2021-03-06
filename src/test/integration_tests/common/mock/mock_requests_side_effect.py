from src.main.video.youtube import const
from src.test.integration_tests.common.mock.dummy_search_response import search_response_01
from src.test.integration_tests.common.mock.dummy_search_response import search_response_02
from src.test.integration_tests.common.mock.dummy_video_response import id_video_response_dict
from src.test.integration_tests.common.mock.dummy_comment_response import id_comment_response_dict
from requests import get


def get_side_effect(uri, query=None):
    if uri == const.END_POINT + '/search':
        if query['pageToken'] is None:
            return type('Response', (object,), {'content': search_response_01})
        else:
            return type('Response', (object,), {'content': search_response_02})
    if uri == const.END_POINT + '/videos':
        return type('Response', (object,), {'content': id_video_response_dict[query['id']]})
    if uri == const.END_POINT + '/commentThreads':
        return type('Response', (object,), {'content': id_comment_response_dict[query['videoId']]})
    return get(uri, query)
