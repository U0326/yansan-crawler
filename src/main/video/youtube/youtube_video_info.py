from src.main.video.youtube import accessor as youtube


class YoutubeVideoInfo:
    @property
    def video_id(self):
        return self.__video_id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def tags(self):
        return self.__tags

    @property
    def comment_of_poster(self):
        return self.__comment_of_poster

    @property
    def published_at(self):
        return self.__published_at

    def __init__(self, video_id):
        video_info = youtube.take_video_info(video_id)
        self.__video_id = video_id
        self.__title = video_info['title']
        self.__description = video_info['description']
        self.__tags = video_info['tags']
        self.__published_at = video_info['publishedAt']
        self.__comment_of_poster = youtube.take_comment_of_poster(video_id)
