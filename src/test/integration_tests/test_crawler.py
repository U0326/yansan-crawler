import logging
from unittest import TestCase
from unittest import mock
from src.main.crawler import video_info
from src.test.integration_tests.mock.mock_requests_side_effect import get_side_effect
from src.main.db.video_repository import *
from src.test.integration_tests.mock.dummy_video_response import id_video_response_dict
from src.test.integration_tests.expected_id_tags import id_tags_dict
import json


# 注) unittestが関数名の昇順に実行されることに依存したコードになっている。
# 注) 実行前にmongodbを起動しておく必要がある。
class TestCrawler(TestCase):
    def setUp(self):
        log_format = '%(asctime)s %(levelname)s %(name)s :%(message)s'
        logging.basicConfig(level=logging.DEBUG, format=log_format)

    @mock.patch('requests.get', side_effect=get_side_effect)
    def test_crawl_01_new_id(self, _):
        video_info.crawl_video_info()
        self._valid_db()

    @mock.patch('requests.get', side_effect=get_side_effect)
    @mock.patch('src.main.crawler.video_info.videoinfo.take_video_info')
    def test_crawl_02_existing_id(self, mock_take_video_info, _):
        video_info.crawl_video_info()
        assert not mock_take_video_info.called
        self._valid_db()

    def _valid_db(self):
        self._valid_video_info()
        self._valid_tags()
        self._valid_processing()

    @staticmethod
    def _valid_video_info():
        documents = list(video_info_collection.find())
        assert len(documents) == 4
        for document in documents:
            response_dict = json.loads(id_video_response_dict[document.get('id')])
            assert response_dict is not None
            assert document.get('title') == response_dict['items'][0]['snippet']['title']
            assert document.get('published_at') == response_dict['items'][0]['snippet']['publishedAt']
            assert set(document.get('tags')) == set(id_tags_dict[document.get('id')])

    @staticmethod
    def _valid_tags():
        documents = list(tags_collection.find())
        assert len(documents) == 16
        for document in documents:
            for _id in document.get('video_id'):
                assert document.get('tag') in id_tags_dict[_id]

    @staticmethod
    def _valid_processing():
        documents = list(processing_collection.find())
        assert len(documents) == 1
        assert documents[0]['next_page_token'] is None
