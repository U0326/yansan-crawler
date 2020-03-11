from src.main.video.niconico import accessor as niconico


class NicoNicoVideoInfo:
    @property
    def description(self):
        return self.__description

    @property
    def tags(self):
        return self.__tags

    def __init__(self, video_id):
        video_info = niconico.take_video_info(video_id)
        self.__description = self.__take_description(video_info)
        self.__tags = self.__take_tags_exclude_category(video_info)

    @staticmethod
    def __take_tags_exclude_category(xml):
        tags = [tag.text for tag in xml.findall('.//tag') if not tag.get('category')]
        return tags

    @staticmethod
    def __take_description(xml):
        description = xml.find('.//description')
        return description.text
