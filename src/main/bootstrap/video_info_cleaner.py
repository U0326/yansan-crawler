import logging

from src.main.video.youtube import accessor
from src.main.db import video_repository

logger = logging.getLogger(__name__)


def cleanup():
    video_ids_on_youtube = accessor.take_all_video_ids()
    video_ids_on_db = video_repository.take_all_video_ids()
    target_video_ids = list(set(video_ids_on_db) - set(video_ids_on_youtube))
    logger.info('Tags [%s] will be removed.', ', '.join(target_video_ids))
    video_repository.delete(target_video_ids)


if __name__ == '__main__':
    cleanup()
