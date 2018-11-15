from conf.bili import Bilibili
from models import VideoFile


class BiliVideoFile(VideoFile):
    '''
    For upload & add single file upon bilibili.com
    '''

    config = Bilibili()
    preupload_params = config.preupload_params
