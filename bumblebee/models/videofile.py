import os


class VideoFile():
    '''
    For upload & add single file upon bilibili.com
    '''

    config = ''
    cu = os.getlogin()
    video_types = (
        '.mp4',
        '.webm',
    )

    def __init__(self, file_name):
        '''
        : param file_name: looks like 'a42b4aa9aa1a47ad8bb2c02a57b60482.mp4'
        '''

        self.name = file_name
        self.URI = file_name.split('.')[0]
        try:
            self.full_path = f'/Users/{self.cu}/{self.config.default_dir}'
        except AttributeError:
            print('need to claim default_dir in CONF!')

        self.full_name = f'{self.full_path}/{file_name}'
        self.size = os.path.getsize(self.full_name)
