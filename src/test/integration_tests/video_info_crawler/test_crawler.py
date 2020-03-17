from unittest import TestCase
from unittest import mock
from src.main.bootstrap import video_info_crawler
from src.test.integration_tests.common.mock.mock_requests_side_effect import get_side_effect
from src.main.db.video_repository import _video_info_collection
from src.main.db.video_repository import _tags_collection
from src.test.integration_tests.common.mock.dummy_video_response import id_video_response_dict
from src.test.integration_tests.video_info_crawler.expected_id_tags import id_tags_dict
import json


# 注) unittestが関数名の昇順に実行されることに依存したコードになっている。
# 注) 実行前にmongodbを起動しておく必要がある。
class TestCrawler(TestCase):
    @mock.patch('requests.get', side_effect=get_side_effect)
    def test_crawl_01_new_id(self, _):
        video_info_crawler.crawl()
        self._valid_db()

    @mock.patch('requests.get', side_effect=get_side_effect)
    @mock.patch('src.main.bootstrap.video_info_crawler.video_info_accessor.take_video_info')
    def test_crawl_02_existing_id(self, mock_take_video_info, _):
        video_info_crawler.crawl()
        assert not mock_take_video_info.called
        self._valid_db()

    def _valid_db(self):
        self.__valid_video_info()
        self.__valid_tags()

    @staticmethod
    def __valid_video_info():
        documents = list(_video_info_collection.find())
        assert len(documents) == 4
        for document in documents:
            response_dict = json.loads(id_video_response_dict[document.get('id')])
            assert response_dict is not None
            assert document.get('title') == response_dict['items'][0]['snippet']['title']
            assert document.get('published_at') == response_dict['items'][0]['snippet']['publishedAt']
            assert set(document.get('tags')) == set(id_tags_dict[document.get('id')])

    @staticmethod
    def __valid_tags():
        documents = list(_tags_collection.find())
        assert len(documents) == 16
        for document in documents:
            for _id in document.get('video_id'):
                assert document.get('tag') in id_tags_dict[_id]
