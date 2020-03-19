from unittest import TestCase
from unittest import mock

from src.main.bootstrap import video_info_crawler
from src.main.bootstrap import video_info_cleaner
from src.test.integration_tests.common.mock.mock_requests_side_effect import get_side_effect
from src.main.db.video_info_collection import _video_info_collection
from src.main.db.tags_collection import _tags_collection

EXISTS_VIDEO_IDS = ['7WJJ_sm2VzM', 'Msg_ArgHetM']
EXPECTED_TAGS = ['れいとしょう', '水島新司', 'マンガ', '山田玲司のヤングサンデー', 'ドカベン', '山田玲司', 'スラムダンク', 'きたがわ翔', '井上雄彦', '漫画', '野球', 'ヤンサン']


# 注) 実行前にmongodbを起動しておく必要がある。
class TestCleaner(TestCase):
    @mock.patch('requests.get', side_effect=get_side_effect)
    def setUp(self, _):
        video_info_crawler.crawl()

    @mock.patch('src.main.bootstrap.video_info_cleaner.accessor.take_all_video_ids',
                return_value=EXISTS_VIDEO_IDS)
    def test_cleanup(self, _):
        video_info_cleaner.cleanup()
        self.__valid_db()

    def __valid_db(self):
        self.__valid_video_info()
        self.__valid_tags()

    @staticmethod
    def __valid_video_info():
        video_info_documents = list(_video_info_collection.find())
        assert len(video_info_documents) == 2
        for video_info_document in video_info_documents:
            assert video_info_document.get('id') in EXISTS_VIDEO_IDS

    @staticmethod
    def __valid_tags():
        tags_documents = list(_tags_collection.find())
        assert len(tags_documents) == 12
        for tags_document in tags_documents:
            assert tags_document.get('tag') in EXPECTED_TAGS
            for video_id in tags_document.get('video_id'):
                assert video_id in EXISTS_VIDEO_IDS
