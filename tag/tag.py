import logging

logger = logging.getLogger(__name__)


def count_tag_appearance(video_info):
    tags = set(video_info.youtube_tags).union(video_info.niconico_tags)
    frequency = {tag: 0 for tag in tags}
    for tag in frequency.keys():
        if tag in video_info.title:
            frequency[tag] += 1
        if tag in video_info.niconico_description:
            frequency[tag] += 1
        if tag in video_info.youtube_description:
            frequency[tag] += 1
    if logger.isEnabledFor(logging.INFO):
        logger.debug('title: ' + video_info.title)
        for k, v in sorted(frequency.items(), key=lambda items: items[1], reverse=True):
            logger.info('tags: ' + k + ' ' + str(v))

    return frequency
