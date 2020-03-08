import logging
from unittest import TestCase
from unittest import mock
from crawler import crawler
from integration_tests.mock.mock_requests_side_effect import get_side_effect
from video.db.video_repository import *
from integration_tests.mock.dummy_video_response import id_video_response_dict
from integration_tests.expected_id_tags import id_tags_dict
import json


# 注) unittestが関数名の昇順に実行されることに依存したコードになっている。
# 注) 実行前にmongodbを起動しておく必要がある。
class TestCrawler(TestCase):
    def setUp(self):
        log_format = '%(asctime)s %(levelname)s %(name)s :%(message)s'
        logging.basicConfig(level=logging.DEBUG, format=log_format)

    @mock.patch('requests.get', side_effect=get_side_effect)
    def test_crawl_01_new_id(self,  *args):
        self.assertEqual(crawler.crawl(), None)
        self._valid_db()

    @mock.patch('requests.get', side_effect=get_side_effect)
    @mock.patch('crawler.crawler.videoinfo.take_video_info')
    def test_crawl_02_existing_id(self, mock_take_video_info, *args):
        crawler.crawl()
        assert not mock_take_video_info.called
        self._valid_db()

    def _valid_db(self):
        self._valid_video_info()
        self._valid_tags()
        self._valid_processing()

    def _valid_video_info(self):
        documents = list(video_info_collection.find())
        assert len(documents) == 4
        for document in documents:
            response_dict = json.loads(id_video_response_dict[document.get('id')])
            assert response_dict is not None
            assert document.get('title') == response_dict['items'][0]['snippet']['title']
            assert document.get('published_at') == response_dict['items'][0]['snippet']['publishedAt']
            assert set(document.get('tags')) == set(id_tags_dict[document.get('id')])

    def _valid_tags(self):
        documents = list(tags_collection.find())
        assert len(documents) == 16
        for document in documents:
            for id in document.get('video_id'):
                assert document.get('tag') in id_tags_dict[id]

    def _valid_processing(self):
        documents = list(processing_collection.find())
        assert len(documents) == 1
        assert documents[0]['next_page_token'] is None
