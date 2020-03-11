import logging
from lxml import etree
import requests
import src.main.video.niconico.config

logger = logging.getLogger(__name__)


def take_vide_info(video_id):
    response = requests.get(src.main.video.niconico.config.END_POINT + '/' + video_id)
    xml_element = etree.XML(response.content)
    logger.debug(etree.tostring(xml_element, encoding="utf-8").decode())
    return xml_element


def take_tags_exclude_category(xml_element):
    tags = [tag.text for tag in xml_element.findall('.//tag') if not tag.get('category')]
    logger.debug('niconico tags: ' + str(tags))
    return tags


def take_description(xml_element):
    description = xml_element.find('.//description')
    return description.text


# TODO 要削除
# if __name__ == '__main__':
#     log_format = '%(asctime)s %(levelname)s %(name)s :%(message)s'
#     logging.basicConfig(level=logging.INFO, format=log_format)
#     xml_element = take_vide_info('so32676256')
#     take_tags_exclude_category(xml_element)
#     take_description(xml_element)
