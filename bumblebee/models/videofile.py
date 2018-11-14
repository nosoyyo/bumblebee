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
        for ext in self.video_types:
            if ext in file_name:
                self.URI = file_name.replace(ext, '')
                self.name = file_name
            else:
                self.URI = file_name
                self.name = f'{file_name}{ext}'
        self.full_name = f'{self.full_path}/{file_name}'
        self.size = os.path.getsize(self.full_name)

        try:
            self.full_path = f'/Users/{self.cu}/{self.config.default_dir}'
        except AttributeError:
            print('need to claim default_dir in CONF!')
