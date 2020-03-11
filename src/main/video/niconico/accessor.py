import logging
from lxml import etree
import requests
from src.main.video.niconico import const

logger = logging.getLogger(__name__)


def take_video_info(video_id):
    response = requests.get(const.END_POINT + '/' + video_id)
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
