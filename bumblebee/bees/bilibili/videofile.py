import os

from config import Bilibili


class VideoFile():
    '''
    For upload & add single file upon bilibili.com
    '''

    config = Bilibili()
    cu = os.getlogin()
    full_path = f'/Users/{cu}/{config.default_dir}'
    preupload_params = config.preupload_params

    def __init__(self, file_name):
        '''
        : param file_name: looks like 'a42b4aa9aa1a47ad8bb2c02a57b60482.mp4'
        '''
        if '.mp4' in file_name:
            self.URI = file_name.replace('.mp4', '')
            self.name = file_name
        else:
            self.URI = file_name
            self.name = f'{file_name}.mp4'
        self.full_name = f'{self.full_path}/{file_name}'
        self.size = os.path.getsize(self.full_name)
