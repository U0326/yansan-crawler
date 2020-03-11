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
